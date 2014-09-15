# Chapter 1, Exercise 3

# An alternative image normalization to histogram equalization is a quotient image. 
# A quotient image is obtained by dividing the image with a blurred version 
# I/(I * Gs). Implement this and try it on some sample images.

from PIL import Image
from pylab import *
from numpy import *
from scipy.ndimage import filters

# params
sigma = 5

# read image
im_color = array(Image.open('data/empire.jpg'))
im_gray = array(Image.open('data/empire.jpg').convert('L'))

# make blurred version of image
# in the color image we need to filter each color channel separately
# tuple passed to filter gives sigma for x, y, and 'cross-color' filtering
# the 'cross-color' filtering should be zero to avoid mixing (gaussian filtering) colors
im_color_blur = filters.gaussian_filter(im_color,[sigma,sigma,0])
im_gray_blur = filters.gaussian_filter(im_gray,sigma)

# check for zeros in blurred image using boolean array
# replace zeros with min value above 0 (find min > 0 using a masked array)
for jj in range(3):
	im_color_blur_zeros = (im_color_blur[:,:,jj] == 0)	# boolean array of zero locations
	maskedarray = ma.masked_where(im_color_blur[:,:,jj] > 0, im_color_blur[:,:,jj])
	im_color_blur[im_color_blur_zeros,jj] = maskedarray.min()

im_gray_blur_zeros = (im_gray_blur == 0)
maskedarray = ma.masked_where(im_gray_blur > 0, im_gray_blur)
im_gray_blur[im_gray_blur_zeros] = maskedarray.min()

# do division
im_color_normed = im_color / im_color_blur
im_gray_normed = im_gray / im_gray_blur

# renormalize result - color
for jj in range(3):
	min_orig = float(im_color[:,:,jj].min())
	max_orig = float(im_color[:,:,jj].max())
	min_new = float(im_color_normed[:,:,jj].min())
	max_new = float(im_color_normed[:,:,jj].max())
	scale_factor = (max_orig - min_orig) / (max_new - min_new)
	im_color_normed[:,:,jj] = scale_factor * (im_color_normed[:,:,jj] - min_new) + min_orig

# renormalize result - grayscale
min_orig = im_gray.min()
max_orig = im_gray.max()
min_new = im_gray_normed.min()
max_new = im_gray_normed.max()
scale_factor = (max_orig - min_orig) / (max_new - min_new)
im_gray_normed = scale_factor * (im_gray_normed - min_new)

# convert back to 8-bit integers 
# necessary for color image, redundant but good practice for grayscale
im_color_normed = uint8(im_color_normed)
im_gray_normed = uint8(im_gray_normed)

# display
fig=figure(figsize=(10,8))
subplot(1,2,1)
axis('off')
imshow(im_color)
subplot(1,2,2)
axis('off')
imshow(im_color_normed)
subplots_adjust(left=0,bottom=0,right=1,top=1,wspace=0,hspace=0)
show()

fig=figure(figsize=(10,8))
gray()
subplot(1,2,1)
axis('off')
imshow(im_gray)
subplot(1,2,2)
axis('off')
imshow(im_gray_normed)
subplots_adjust(left=0,bottom=0,right=1,top=1,wspace=0,hspace=0)
show()
