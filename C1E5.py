# Chapter 1, Exercise 5
# Implement a line detection algorithm; highlight line.

from PIL import Image
from pylab import *
from numpy import *
from scipy.ndimage import filters
from scipy.ndimage import measurements,morphology
import imtools

# read image
im = array(Image.open('data/empire.jpg').convert('L'))
xsize,ysize = im.shape

# set threshold
gradthreshold = 256

# calculate gradients and threshold
imx = zeros(im.shape)
filters.sobel(im,1,imx)
imy = zeros(im.shape)
filters.sobel(im,0,imy)
gradmag = sqrt(imx**2+imy**2)
gradang = arctan2(imx,imy)

# walk through all points
# if grad > threshold, get angle, step in that direction
# if point in that direction still has gradient > threshold
# and if angle is the same, continue
# if number of points > threshold, consider it a line
# highlight those points (could also plot line)
# continue from orignal point unless point was already examined

gradangles = 0
gradpointcount = 0
for i in range(0,xsize):
	for j in range(0,ysize):
		if gradmag[i,j] > gradthreshold:
			gradangles += gradang[i,j]
			gradpointcount += 1

print "Counted grad points: ", gradpointcount
print "Grad angle average is ", gradangles/gradpointcount
print "Mean grad angle is ", gradang.mean()

#gradmag = 1*(gradmag>gradthreshold)
# find objects from gradient
#labels,nbr_objects = measurements.label(gradmag)
#print "Number of objects:", nbr_objects

#display original, gradient
figure()
gray()
subplot(1,2,1)
axis('off')
imshow(im)
subplot(1,2,2)
imshow(gradang)
axis('off')
subplots_adjust(left=0,right=1,bottom=0,top=1,wspace=0,hspace=0)
show()
