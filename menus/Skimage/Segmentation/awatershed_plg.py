# -*- coding: utf-8 -*
from imagepy.core.engine import Filter
from skimage.filters import gaussian
from skimage.morphology import watershed, disk
from skimage.filters import rank
import numpy as np
from scipy import ndimage as ndi
from imagepy import IPy

class Plugin(Filter):
	title = 'Active Watershed'
	note = ['8-bit', 'not_slice', 'auto_snap', 'not_channel']
	
	para = {'sigma':2, 'gdt':2}
	view = [(int, (0,10), 0,  'sigma', 'sigma', 'pix'),
			(int, (0, 10), 0,  'gradient', 'gdt', '')]
	
	def run(self, ips, snap, img, para = None):
		denoised = rank.median(img, disk(para['sigma']))
		gradient = rank.gradient(denoised, disk(para['gdt']))
		markers, n = ndi.label(ips.get_msk(), np.ones((3,3)))
		labels = watershed(gradient, markers, watershed_line=True)
		img[:] = np.where(labels==0, 255, img*0.5)