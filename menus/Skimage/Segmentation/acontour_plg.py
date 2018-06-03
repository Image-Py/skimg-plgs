# -*- coding: utf-8 -*
from imagepy.core.engine import Simple
from skimage.filters import gaussian
from skimage.segmentation import active_contour
import numpy as np
from imagepy.core.roi import PolygonRoi
from imagepy import IPy

class Plugin(Simple):
	title = 'Snake'
	note = ['all', 'req_roi']
	
	para = {'sigma':3.0, 'alpha':0.015, 'beta':10, 'gamma':0.001}
	view = [(float, 'sigma',(0,10), 1,  'sigma',  'pix'),
		(float, 'alpha',(0.001, 0.01), 3,  'alpha',  ''),
		(float,  'beta',(0,30), 0,  'beta', ''),
		(float,  'gamma',(0.001, 0.01), 3,  'gamma', '')]

	def load(self, ips):
		if not isinstance(ips.roi, PolygonRoi) or len(ips.roi.body)!=1:
			IPy.alert('active contour need a polygon roi with single circle')
		else: return True

	def run(self, ips, imgs, para = None):
		pts = np.array(ips.roi.body[0][0])
		snake = active_contour(gaussian(ips.img, 3), pts, 
			alpha=para['alpha'], beta=para['beta'], gamma=para['gamma'])
		ips.roi = PolygonRoi([[[tuple(i) for i in snake],[]]])