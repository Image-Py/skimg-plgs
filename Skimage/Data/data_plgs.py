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