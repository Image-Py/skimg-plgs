from skimage.filters import roberts, sobel, scharr, prewitt
from imagepy.core.engine import Filter

class Roberts(Filter):
    title = 'Roberts'
    note = ['all', 'auto_msk', 'auto_snap']

    def run(self, ips, snap, img, para = None):
        return roberts(snap)*255
        
class Sobel(Filter):
    title = 'Sobel'
    note = ['all', 'auto_msk', 'auto_snap']

    def run(self, ips, snap, img, para = None):
        return sobel(snap)*255

class Scharr(Filter):
    title = 'Scharr'
    note = ['all', 'auto_msk', 'auto_snap']

    def run(self, ips, snap, img, para = None):
        return scharr(snap)*255

class Prewitt(Filter):
    title = 'Prewitt'
    note = ['all', 'auto_msk', 'auto_snap']

    def run(self, ips, snap, img, para = None):
        return prewitt(snap)*255

plgs = [Roberts, Sobel, Scharr, Prewitt]