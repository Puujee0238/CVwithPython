# Chapter 1, Exercise 2
# Implement unsharp masking to an image (both color and grayscale)

from PIL import Image
from pylab import *
from numpy import *
from scipy.ndimage import filters
import imtools

# read image
im = array(Image.open('data/empire.jpg').convert('L'))

# make high-contrast version
# imhc, cdf = imtools.histeq(im)

# make unsharp mask
imblur = filters.gaussian_filter(im,0)
immask = im - imblur

# apply mask
imsharp1 = im + 1.0*immask
imsharp2 = im + 0.67*immask
imsharp3 = im + 0.33*immask

#display original and filter
figure()
gray()
subplot(2,2,1)
axis('off')
imshow(im)
subplot(2,2,2)
imshow(imsharp1)
axis('off')
subplot(2,2,3)
imshow(imsharp2)
axis('off')
subplot(2,2,4)
imshow(imsharp3)
axis('off')
subplots_adjust(left=0,right=1,bottom=0,top=1,wspace=0,hspace=0)
show()