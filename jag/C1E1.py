# Take an image and apply Gaussian blur like in Figure 1.9. Plot the image
# contours for increasing values of  sigma. What happens? Can you explain why?

from PIL import Image
from numpy import *
from pylab import imshow, show, gray
from scipy.ndimage import filters

im = array(Image.open('data/empire.jpg').convert('L'))
gray()

sigma = 1
imshow(filters.gaussian_filter(im, sigma))

show()
