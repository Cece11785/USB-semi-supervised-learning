import PIL
from PIL import Image
import PIL, PIL.ImageOps, PIL.ImageEnhance, PIL.ImageDraw
import numpy as np

def Cutout(img, ratio, color, position):
    if ratio < 0:
        return img

    w, h = img.size
    ratio=np.sqrt(ratio)
    sizew = ratio * img.size[0]
    sizeh=ratio * img.size[1]

    x0 = np.random.uniform(w)
    y0 = np.random.uniform(h)

    x0 = int(max(0, x0 - sizew / 2.))
    y0 = int(max(0, y0 - sizeh / 2.))
    x1 = min(w, x0 + sizew)
    y1 = min(h, y0 + sizeh) 

    xy = (x0, y0, x1, y1)
    img = img.copy()
    PIL.ImageDraw.Draw(img).rectangle(xy, color)
    return img

class MaskAugment:
    """
    mask_ratio: str or float (0., 1.), ratio of mask wrt. image size, or 'random'
    mask_color: str or tuple, specify color in 3 channels, or 'average' for average of this image
    mask_position: str, defaults to and only supports 'random'
    """
    def __init__(self, mask_ratio='random', mask_npatch=1.0, mask_color=(0, 0, 0), mask_position='random'):
        self.mask_ratio = mask_ratio
        self.mask_npatch= mask_npatch
        self.mask_color = tuple([int(c) for c in mask_color])
        self.mask_position = mask_position

    def __call__(self, img):
        if self.mask_ratio == "random":
            self.mask_ratio = random.random() * 0.5 

        assert 0 <= self.mask_ratio < 1
        mask_ratio_perpatch=self.mask_ratio/self.mask_npatch
        for i in range(int(self.mask_npatch)):
            img = Cutout(img, mask_ratio_perpatch, self.mask_color, self.mask_position)
        return img

if __name__ == '__main__':
    import os

    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    img = Image.open('./u.jpg')
    randaug = MaskAugment(0.2)
    img = randaug(img)
    import matplotlib
    from matplotlib import pyplot as plt 
    plt.imshow(img)
    plt.show()
