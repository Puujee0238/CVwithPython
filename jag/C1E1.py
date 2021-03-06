
# Take an image and apply Gaussian blur like in Figure 1.9. Plot the image
# contours for increasing values of sigma. What happens? Can you explain why?

import sys
from PIL import Image
from numpy import array
from pylab import imshow, show, gray, figure, contour, axis
from scipy.ndimage import filters

sigma = 1
if len(sys.argv) > 1:
    sigma = int(sys.argv[1])

im = array(Image.open('data/empire.jpg').convert('L'))
im2 = filters.gaussian_filter(im, sigma)
figure()
gray()

# imshow(im2)
contour(im2, origin='image')
axis('equal')
axis('off')

show()
