from imagepy.core.engine import Filter
from skimage.morphology import watershed
from skimage.filters import sobel

class Plugin(Filter):
    title = 'Up And Down Watershed'
    note = ['8-bit', 'auto_msk', 'auto_snap', 'preview']
    
    para = {'thr1':0, 'thr2':255}
    view = [('slide', (0,255), 0, 'Low', 'thr1'),
            ('slide', (0,255), 0, 'High', 'thr2')]

    def load(self, ips):
        self.buflut = ips.lut
        ips.lut = ips.lut.copy()
        return True
    
    def preview(self, ips, para):
        ips.lut[:] = self.buflut
        ips.lut[:para['thr1']] = [0,255,0]
        ips.lut[para['thr2']:] = [255,0,0]
        ips.update = 'pix'

    #process
    def run(self, ips, snap, img, para = None):
        edge = sobel(snap)
        img[:] = 0
        img[snap>para['thr2']] = 2
        img[snap<para['thr1']] = 1
        ips.lut = self.buflut
        return (watershed(edge, img)==2) * 255
