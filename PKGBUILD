# Maintainer: Serge Koval <serge.koval@gmail.com>

pkgname=rofi-clip
pkgver=0.3
pkgrel=1
pkgdesc="Clipboard manager to use with rofi"
arch=('x86_64')
url="https://github.com/mrjoes/rofi-clip"
license=('GPL')
groups=()
depends=("python" "clipnotify" "xclip" "xdotool")
makedepends=()
checkdepends=()
optdepends=('rofi' 'dmenu')
provides=("rofi-clip")
conflicts=()
replaces=()
backup=()
options=('!strip')
source=("rofi-clip.py" "rofi-clip.service")
noextract=()
sha256sums=('dabbf16847a42b535412b5e72d688edf899b3837adbb2f4d198077c1ecaae46b'
	    '7ebaf81bbdb10cddd043f588943e3c2cd71aa29f244989e62b76b709c44af5e9')

package() {
        install -Dm755 rofi-clip.py "$pkgdir/usr/bin/rofi-clip"
        install -Dm644 "$srcdir/rofi-clip.service" "$pkgdir/usr/lib/systemd/user/rofi-clip.service"
}

