# Chapter 1, Exercise 1
# Apply gaussian blur to an image per Fig 1.9; plot contours 
# for increaseing sigma. What happens and why?

# Answer: contours get spaced farther apart; detail disappears
# The blur is erasing sharp edges, making contours less distinct.
# The algorithm for contour() must have a threshold for gradient
# that identifies contours; falling below this gradient level
# turns off that location as a contour.

from PIL import Image
from pylab import *
from numpy import *
from scipy.ndimage import filters
import imtools

# read image
im = array(Image.open('data/empire.jpg').convert('L'))

# apply filter
im2 = filters.gaussian_filter(im,5)

#display original and filter
figure()
gray()
subplot(2,2,1)
imshow(im)
subplot(2,2,2)
imshow(im2)
subplot(2,2,3)
contour(im,origin='image')
subplot(2,2,4)
contour(im2,origin='image')
#axis('equal')
#axis('off')
show()