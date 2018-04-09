skimg-plgs   
======================


**Introduction:**scikit-image need not much introductions, It is a famous Python imageprocessing library. ImagePy is a interactive image processing framework which can wrap any numpy based library esaily. And supporting multi-channels, imagestack, lookuptable, roi, macros recorder...It is a Plugin system(just like ImageJ but more convenient). This project is a wrapper of scikit-image for ImagePy plugins!

**Now It is just a start, I wrap little of scikit-image's algrism, aimed to introduct how to wrote ImagePy plugin, The Demo in this document is representative.**

License
-------
I know many numpy based project has a BSD license, but, sorry, I use wxpython as ui framework, so, must be under LGPL.

MainFrame
---------
![mainframe](http://skimgplgs.imagepy.org/mainframe.png)

It is ImagePy's MainFrame, like ImageJ. And ImagePy has contains many common function, such as open image, save image, do some filter, do a roi, draw with pencil... It requires wxpython as ui, Numpy as base structure, shapely to treat the roi, and scipy.ndimage to so dome common filter. But this project devotes to **do a full wrapper for scikit-image**.


Open a simple data in ImagePy
-----------------------
![opendata](http://skimgplgs.imagepy.org/opendata.png)
Skimage > data
```python
from imagepy import IPy
from imagepy.core.engine import Free
from skimage import data

class Plugin(Free):
    title = 'astronaut'

    def run(self, para = None):
        IPy.show_img([data.astronaut()], self.title)
```
1. Class must be named Plugin extend Free
2. title is necessary, be the plugin's id, show in menus.
3. Overwrite the run, do what you want.

"Free" is a engine of ImagePy, (5 engines in total), meas depend on nothing, 
we can open a Image in any case! We just need override the run method, and show the image in run. IPy is the util class to show image, show table, write log, and show dialog...

```python
from imagepy import IPy
from imagepy.core.engine import Free
from skimage import data

class Data(Free):
    def __init__(self, title):
        self.title = title
        self.data = getattr(data, title)

    def run(self, para = None):
        IPy.show_img([self.data()], self.title)

    def __call__(self):
        return self

datas = ['page', 'astronaut', 'horse', 'camera', 
    'hubble_deep_field', 'coins', 'immunohistochemistry', 'moon']

plgs = [Data(i) for i in datas]
```
Show a image is too simple that it's fussy to create a new script for every image. We can write these class in one file and name the class arbitrarily, but put them in a list named **plgs**, what more, ImagePy will call Class().run() when it is impulsed, so we can overwrite then call mathod to return itself. Then we do a data opener plugin in several lines, which can open all the  skimage's Simple data.

Do a simple filter
------------------
![simplefilter](http://skimgplgs.imagepy.org/simplefilter.png)
```python
from skimage.filters import roberts, sobel, scharr, prewitt
from imagepy.core.engine import Filter

class Roberts(Filter):
    title = 'Roberts'
    note = ['all', 'auto_msk', 'auto_snap']

    def run(self, ips, snap, img, para = None):
        return roberts(snap)*255
        
class Sobel(Filter):
    ......

class Scharr(Filter):
    ......

class Prewitt(Filter):
    ......

plgs = [Roberts, Sobel, Scharr, Prewitt]
```
### These gradient operator is simplest filter with no parameter.
1. title is necessary
2. set the note, which tells ImagePy what to do for you.
3. overwrite run method return the result

Filter means need a image, then do some change on it, It has a run method in such type:
* **ips** is the wrapper of image with some other information (lookup table, roi...)
* **snap** is a snapshot of the image, if 'auto_snap' in note, ImagePy will copy the image to snap befor run. (for many filter method must be implemented in a buffer)
* **img** is the current image you are processing.
* **para** is the parameter you got interactive. (there is no here)
### note is very important

* **all** means this plugin works for all type image.
* **auto_snap** means ImagePy do a snapshot befor processing, then you can use Undo.
* **auto_msk** means when there is a roi on the image, Plugin will only influnce the pixel in.
* more detail information please see [ImagePy's README](https://github.com/Image-Py/imagepy)!


![colorfilter](http://skimgplgs.imagepy.org/colorfilter.png)
You see, we didnot write code to treat the color image, but it works, and We can draw a ROI on the image, only the ROI area be changed! And we can undo the lasted operation. **Even if it is a imagestack, ImagePy will ask you if run every slice!!**

Filter with parameter
---------------------
![canny](http://skimgplgs.imagepy.org/canny.png)
```python
# -*- coding: utf-8 -*
from skimage import feature
from imagepy.core.engine import Filter

class Plugin(Filter):
    title = 'Canny'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'sigma':1.0, 'low_threshold':10, 'high_threshold':20}
    view = [(float, (0,10), 1,  'sigma', 'sigma', 'pix'),
            ('slide',(0,30), 4, 'low_threshold', 'low_threshold'),
            ('slide',(0,30), 4, 'high_threshold', 'high_threshold')]

    def run(self, ips, snap, img, para = None):
        return feature.canny(snap, sigma=para['sigma'], low_threshold=para[
            'low_threshold'], high_threshold=para['high_threshold'], mask=ips.get_msk())*255
```
Many Filter need some parameter. Just like Canny. We just need do a little more.
1. **para** is a dict object, which contains the parameter you need.
2. **view** tell ImagePy how to interact when this plugin run, **(float, (0,10), 1, 'sigma', 'sigma', 'pix')** means it is a float between 0 and 10, title is sigma, corresponding to the sigma parameter with unit pix. 
More detail information please see [ImagePy's README](https://github.com/Image-Py/imagepy)!

**Add 'preview' in note, then when you adjust the parameter, ImagePy run this plugin immediately**

Watershed with up and down threshold as marker
--------------------------------------------
![threshold watershed](http://skimgplgs.imagepy.org/thrwatershed.png)
```python
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
    
    def preview(self, para):
        self.ips.lut[:] = self.buflut
        self.ips.lut[:para['thr1']] = [0,255,0]
        self.ips.lut[para['thr2']:] = [255,0,0]
        self.ips.update = 'pix'

    #process
    def run(self, ips, snap, img, para = None):
        edge = sobel(snap)
        img[:] = 0
        img[snap>para['thr2']] = 2
        img[snap<para['thr1']] = 1
        ips.lut = self.buflut
        return (watershed(edge, img)==2) * 255
```
This plugin is a little specific.
1. **load** run befor the run function, And if it return False, The plugin will be interupted! here we copy the look up tabel.
2. **preview** run when 'preview' tag in note, and the parameter is changed. In defalt call the run method, but now we can overwrite it to change the lookup table.


Then use the marker interactive to run watershed algrism, do not forget put the old lookup table back! else the Image will in red-green color map.

**We use '8-bit' in note because watershed algrism doesnot work for color image, use '8-bit', '16-bit' instead of 'all', ImagePy will check the type befor run, and interupt immediately if not match!**

Watershed with interactive marker
---------------------------------
![interactive watershed](http://skimgplgs.imagepy.org/interwatershed.png)
```python
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
```
ImagePy support ROI, you can use tool to draw a roi(point, line, polygon...), And We can use ips.roi access it, and ips.get_msk(mode='in') to get the roi mask image. **mode can be 'in','out',or int means a sketch with specific width.** Then use the mask as marker to do a watershed, we got a perfect result!

**We add 'not_slice', 'not_channel' in note, it tells Imagepy need not to iterate each channel and do stack for us, because this interactive is ok for specific image, there is no need to go through**

Interactive Countours
---------------------
![interactive countours](http://skimgplgs.imagepy.org/snake.png)
```python
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
	view = [(float, (0,10), 1,  'sigma', 'sigma', 'pix'),
		(float, (0.001, 0.01), 3,  'alpha', 'alpha', ''),
		(float, (0,30), 0,  'beta', 'beta', ''),
		(float, (0.001, 0.01), 3,  'gamma', 'gamma', '')]

	def load(self, ips):
		if not isinstance(ips.roi, PolygonRoi) or len(ips.roi.body)!=1:
			IPy.alert('active contour need a polygon roi with single circle')
		else: return True

	def run(self, ips, imgs, para = None):
		pts = np.array(ips.roi.body[0][0])
		snake = active_contour(gaussian(ips.img, 3), pts, 
			alpha=para['alpha'], beta=para['beta'], gamma=para['gamma'])
		ips.roi = PolygonRoi([[[tuple(i) for i in snake],[]]])
```
1. **req_roi** means this plugin need a roi, ImagePy will check for you, if ther is not, interrupt the plugin.
2. **load** we check if the roi is a single circle, else return False to interrupt

**Simple** is another engine, with a type below:
* **ips** is the wrapper of image.
* **imgs** is the hole image sequence of ips.

**It means do something not for every slice, such as set the roi or lookup table. And If you want do a 3D filter, please extend a Simple. Filter is just for slice.**

Treat fragments and Mesure
--------------------------
continued from the interactive threshold watershed demo

![fragment](http://skimgplgs.imagepy.org/fragment.png)

![measure](http://skimgplgs.imagepy.org/measure.png)
```python
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

```
We do a morphology to remove the small fragments and fill the holes, then Do a Region Analysis. Draw a mark on the image and generate a table. We can export excel file from the table's file menu.

The Analysis plugin is in ImagePy > Analysis, be cause we must construct the regionprops, The code is a little long. But We can Use IPy.Table, IPy.write to generate table and log esaily!

Macros
------
![record](http://skimgplgs.imagepy.org/record.png)

**Macros** is the fourth engine, It is a text file with every line as:
**"PluginID > {parameter}"**, If the parameter is None and the Plugin need parameter, IPy will show dialog to interact, if the parameter is given, ImagePy just run use the given parameter.

We can Open the **Plugin > Macros > Macros Recorder** to record the operate. Then save as a file with **.mc** extent under the menus folder. It will be parsed as a menu when started next. This is Macros, We never need to implements ourself.

![macros](http://skimgplgs.imagepy.org/macros.png)

Then we Try the **Coins Segment And Measure** macros, Wow!, It run the command sequence automatically!

**We can use Macros to do some bat processing, what more? It can be used as  a good tutorial, We just implement the baseic method, and use macros to show this method can solve such problem!!!**

Tool
----
**Tool** is the last engine. It need to overwrite some mouse envent, and a logo shown in toolbox. ImagePy has supported many tools, draw, selection, transform... if necessary, you can extend a tool.

**more detail information please see [ImagePy's README](https://github.com/Image-Py/imagepy)!**

About the plugin's order
------------------------
![catlog](http://skimgplgs.imagepy.org/catlog.png)

ImagePy is a plugin framework. The Catlog will be parsed as the corresponding menus. You just copy package under the menus folder or it's sub folder. But the question is, Our function will be in a disordered order. **So we can add a list called catlog under every init file.**

![plugins](http://skimgplgs.imagepy.org/plugins.png)

Now Skimage menu is before the Help, and the Data is the first Item, then Filter, Morphology, Segmentation, last is Demo. and if we put '-' in catlog, It will be parsed as a spliter line.

**OK! That is a start, I want more developer can join. I think it is significative to let scikit-image be esaier to approach, Benifit more scientists who does not master programming. But I cannot do it by myself, My English is not so good, and have little spare time, But I will do my best!** 