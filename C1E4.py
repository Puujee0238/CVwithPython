# Chapter 1, Exercise 4
# Implment a simple object detection function using gradients.

from PIL import Image
from pylab import *
from numpy import *
from scipy.ndimage import filters
from scipy.ndimage import measurements,morphology
import imtools

# read image
im = array(Image.open('data/empire.jpg').convert('L'))

# set threshold
gradthreshold = 16

# calculate gradients and threshold
#GradX = roll(U,-1,axis=1)-U   # x component of U gradient
#GradY = roll(U,-1,axis=0)-U   # y component
#tGradX = 1*(GradX > gradthreshold)
#tGradY = 1*(GradY > gradthreshold)
imx = zeros(im.shape)
filters.sobel(im,1,imx)
imy = zeros(im.shape)
filters.sobel(im,0,imy)
gradmag = sqrt(imx**2+imy**2)
gradmag = 1*(gradmag>gradthreshold)

# find objects from gradient
labels,nbr_objects = measurements.label(gradmag)
print "Number of objects:", nbr_objects

#display original, gradient
figure()
gray()
subplot(1,2,1)
axis('off')
imshow(im)
subplot(1,2,2)
imshow(gradmag)
axis('off')
subplots_adjust(left=0,right=1,bottom=0,top=1,wspace=0,hspace=0)
show()