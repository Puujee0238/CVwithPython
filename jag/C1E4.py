# Write a function that finds the outline of simple objects in images (for
# example a square against white background) using image gradients.


import argparse
from PIL import Image
from numpy import array, zeros, uint8, sqrt
from pylab import imshow, show, gray, figure, contour, axis
from scipy.ndimage import filters


parser = argparse.ArgumentParser(description='Apply unsharp filter.')
parser.add_argument('sigma', metavar='sigma', type=int, default=1,
                   nargs='?', help='Sigma for gaussian blue')
parser.add_argument('scale', metavar='scale', type=float, default=0.1,
                   nargs='?', help='scale for gaussian subtraction')

args = parser.parse_args()

raw_image = Image.open('data/detect_lines1.png').convert('L')
im = array(raw_image)
print im.shape, im.dtype

#Sobel derivative filters
imx = zeros(im.shape)
filters.sobel(im,1,imx)
imy = zeros(im.shape)
filters.sobel(im,0,imy)
magnitude = sqrt(imx**2+imy**2)

figure()
gray()
imshow(magnitude)
show()
