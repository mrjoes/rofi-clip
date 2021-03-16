# Maintainer: Serge Koval <serge.koval@gmail.com>

pkgname=rofi-clip
pkgver=0.2
pkgrel=1
pkgdesc="Clipboard manager to use with rofi"
arch=('x86_64')
url="https://github.com/mrjoes/rofi-clip"
license=('GPL')
groups=()
depends=("python" "xclip" "python-pyperclip" "xdotool")
makedepends=()
checkdepends=()
optdepends=('rofi' 'fzf' 'dmenu')
provides=("rofi-clip")
conflicts=()
replaces=()
backup=()
options=('!strip')
source=("rofi-clip.py" "rofi-clip.service")
noextract=()
sha256sums=('f628fbbb97ec2dc3b01bb16013458fa4e2757ee1323e377beaed538756358723'
	    '7ebaf81bbdb10cddd043f588943e3c2cd71aa29f244989e62b76b709c44af5e9')

package() {
        install -Dm755 rofi-clip.py "$pkgdir/usr/bin/rofi-clip"
        install -Dm644 "$srcdir/rofi-clip.service" "$pkgdir/usr/lib/systemd/user/rofi-clip.service"
}

