#!/usr/bin/python
import os
import subprocess
import socket
import json
import struct
from select import select
from threading import Thread, Lock
from sys import argv


# Settings
CLIP_LIMIT = 200             # number of clipboard history
STRING_LIMIT = 200
HELP = '''rofi-clip menu|daemon'''
CLIP_GET = ["xclip", "-o", "-selection", "clipboard"]
CLIP_SET = ["xclip", "-selection", "clipboard"]
PASTE = "xdotool key ctrl+shift+v"


class ClipboardManager():
    def __init__(self):
        self.selected = None
        self.clips = []
        self.lock = Lock()

    def _server_address(self):
        return os.environ['XDG_RUNTIME_DIR'] + '/rofi-clip.sock'

    def _send(self, conn, payload):
        raw = json.dumps(payload).encode('utf-8')
        pack_len = struct.pack("!i", len(raw))

        conn.send(pack_len)
        conn.send(raw)

    def _recv(self, conn):
        data = conn.recv(4)
        pack_len = struct.unpack("!i", data)[0]

        data = conn.recv(pack_len)
        return json.loads(data)

    def _communicate(self, msg):
        conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        conn.connect(self._server_address())

        self._send(conn, msg)
        return self._recv(conn)

    def _send_current(self, conn):
        if self.selected is not None and self.selected < len(self.clips):
            self._send(conn, self.clips[self.selected])
        else:
            self._send(conn, '')

    def _clip_get(self):
        process = subprocess.Popen(CLIP_GET, stdout=subprocess.PIPE)
        return process.stdout.read().decode('utf-8')

    def _clip_set(self, text):
        process = subprocess.Popen(CLIP_SET, stdin=subprocess.PIPE)
        process.stdin.write(text.encode('utf-8'))

    def _paste(self, text):
        if text:
            # Paste selection
            self._clip_set(text)

            # Insert
            os.system(PASTE)

    def server_loop(self):
        print('Started RPC server...')

        server_address = self._server_address()

        try:
            os.unlink(server_address)
        except OSError:
            if os.path.exists(server_address):
                raise

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(server_address)
        sock.listen(1)

        while True:
            conn, _ = sock.accept()

            try:
                msg = self._recv(conn)
                if msg['op'] == 'clips':
                    with self.lock:
                        self._send(conn, self.clips)
                        self.selected = None
                elif msg['op'] == 'set':
                    with self.lock:
                        self.selected = msg['select']
                        self._send_current(conn)
                elif msg['op'] == 'paste':
                    with self.lock:
                        self._send_current(conn)
                else:
                    self._send(conn, False)
            except:
                import traceback
                traceback.print_exc()
            finally:
                conn.close()

    def clip_loop(self):
        print('Started clip loop...')

        while True:
            os.system('clipnotify')

            with self.lock:
                clip = self._clip_get()
                if clip and (not self.clips or clip != self.clips[0]):
                    if clip in self.clips:
                        self.clips.remove(clip)
                    self.clips.insert(0, clip)

                while len(self.clips) > CLIP_LIMIT:
                    self.clips = self.clips[:-1]

    def daemon(self):
        t = Thread(target=self.clip_loop)
        t.daemon = True
        t.start()

        self.server_loop()

    def menu(self):
        clips = self._communicate({'op': 'clips'})

        for index, clip in enumerate(clips):
            clip = clip.replace('\n', ' ')
            print('{}: {}'.format(index, clip[0:STRING_LIMIT]))

    def copy(self, select):
        if select:
            index = int(select[0:select.index(':')])
            self._communicate({'op': 'set', 'select': index})

    def paste(self):
        text = self._communicate({'op': 'paste'})
        self._paste(text)

if __name__ == "__main__":
    cm = ClipboardManager()

    if len(argv) <= 1:
        print(HELP)
    elif argv[1] == 'daemon':
        cm.daemon()
    elif argv[1] == 'menu' and len(argv) == 2:
        cm.menu()
    elif argv[1] == 'menu' and len(argv) > 2:
        cm.copy(argv[2])
    elif argv[1] == 'paste':
        cm.paste()
    else:
        print(HELP)

    exit(0)

