# Chapter 1, Exercise 2

# Implement an unsharp masking operation (http://en.wikipedia.org/wiki/Unsharp_ masking) 
# by blurring an image and then subtracting the blurred version from the original. 
# This gives a sharpening effect to the image. Try this on both color and grayscale images.

from PIL import Image
from pylab import *
from numpy import *
from scipy.ndimage import filters

# read image
im_color = array(Image.open('data/prometheus.jpg'))
im_gray = array(Image.open('data/prometheus.jpg').convert('L'))

# make unsharp mask by blurring
# in the color image we need to filter each color channel separately
# tuple passed to filter gives sigma for x, y, and 'cross-color' filtering
# the 'cross-color' filtering should be zero to avoid mixing (gaussian filtering) colors
im_color_blur = filters.gaussian_filter(im_color,[3,3,0])
im_gray_blur = filters.gaussian_filter(im_gray,3)

# apply mask - empirically choose constant
im_color_sharp = im_color - 0.5*im_color_blur
im_gray_sharp = im_gray - 0.5*im_gray_blur

# renormalize result - color
for jj in range(3):
	min_orig = float(im_color[:,:,jj].min())
	max_orig = float(im_color[:,:,jj].max())
	min_new = float(im_color_sharp[:,:,jj].min())
	max_new = float(im_color_sharp[:,:,jj].max())
	scale_factor = (max_orig - min_orig) / (max_new - min_new)
	im_color_sharp[:,:,jj] = scale_factor * (im_color_sharp[:,:,jj] - min_new) + min_orig

# renormalize result - grayscale
min_orig = im_gray.min()
max_orig = im_gray.max()
min_new = im_gray_sharp.min()
max_new = im_gray_sharp.max()
scale_factor = (max_orig - min_orig) / (max_new - min_new)
im_gray_sharp = scale_factor * (im_gray_sharp - min_new)

# convert back to 8-bit integers 
# necessary for color image, redundant but good practice for grayscale
im_color_sharp = uint8(im_color_sharp)
im_gray_sharp = uint8(im_gray_sharp)

#display original and sharpened version (color)
fig1=figure(figsize=(8,8))
subplot(2,1,1)
axis('off')
imshow(im_color)
subplot(2,1,2)
axis('off')
imshow(im_color_sharp)
subplots_adjust(left=0,right=1,bottom=0,top=1,wspace=0,hspace=0)
show()

#display original and sharpened version (grayscale)
fig1=figure(figsize=(8,8))
gray()
subplot(2,1,1)
axis('off')
imshow(im_gray)
subplot(2,1,2)
axis('off')
imshow(im_gray_sharp)
subplots_adjust(left=0,right=1,bottom=0,top=1,wspace=0,hspace=0)
show()