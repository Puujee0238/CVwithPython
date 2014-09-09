# Chapter 1, Exercise 6
# Apply label() to an image; use histograms and label image 
# to plot distribution of object sizes.

from PIL import Image
from pylab import *
from numpy import *
from scipy.ndimage import filters
from scipy.ndimage import measurements,morphology
import imtools

# read image
im = array(Image.open('data/empire.jpg').convert('L'))

# set threshold
threshold = 196

# threshold image
im = 1*(im<threshold)
labels, nbr_objects = measurements.label(im)
print "Number of objects:", nbr_objects

#display original, gradient
figure()
gray()
subplot(1,3,1)
axis('off')
imshow(im)
subplot(1,3,2)
axis('off')
imshow(labels)
subplot(1,3,3)
hist(labels.flatten(),0.25*nbr_objects)
#subplots_adjust(left=0,right=1,bottom=0,top=1,wspace=0,hspace=0)
show()
