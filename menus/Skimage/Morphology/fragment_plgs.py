from imagepy.core.engine import Filter
from skimage.morphology import remove_small_objects
from skimage.morphology import remove_small_holes

class RemoveObjects(Filter):
    title = 'Remove Small Objects'
    note = ['8-bit', 'auto_msk', 'auto_snap', 'preview']
    
    para = {'size': 64, 'con':2}
    view = [(int, (0,1e8), 0, 'size', 'size', 'pix'),
            (int, (1,3), 0, 'connect', 'con', '')]

    #process
    def run(self, ips, snap, img, para = None):
        msk = remove_small_objects(snap>0, para['size'], para['con'])
        img[:] = msk * 255

class RemoveHoles(Filter):
    title = 'Remove Small Holes'
    note = ['8-bit', 'auto_msk', 'auto_snap', 'preview']
    
    para = {'size': 64, 'con':2}
    view = [(int, (0,1e8), 0, 'size', 'size', 'pix'),
            (int, (1,3), 0, 'connect', 'con', '')]

    #process
    def run(self, ips, snap, img, para = None):
        msk = remove_small_holes(snap>0, para['size'], para['con'])
        img[:] = msk * 255

plgs = [RemoveObjects, RemoveHoles]