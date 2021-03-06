# An alternative image normalization to histogram equalization is a quotient
# image. A quotient image is obtained by dividing the image with a blurred
# version I/(I * G ). Implement this and try it on some sample images.

# XXX: This is not working.

import argparse
from PIL import Image
from numpy import array, zeros, uint8
from pylab import imshow, show, gray, figure, contour, axis
from scipy.ndimage import filters


parser = argparse.ArgumentParser(description='Apply unsharp filter.')
parser.add_argument('sigma', metavar='sigma', type=int, default=1,
                   nargs='?', help='Sigma for gaussian blue')
parser.add_argument('scale', metavar='scale', type=float, default=0.1,
                   nargs='?', help='scale for gaussian subtraction')
parser.add_argument('--bw', dest='blackwhite', action='store_true',
                   help='use a black and white image.')

args = parser.parse_args()

raw_image = Image.open('data/empire.jpg')
if args.blackwhite:
  raw_image = raw_image.convert('L')
im = array(raw_image)

if args.blackwhite:
  im2 = filters.gaussian_filter(im, args.sigma)
else:
  im2 = zeros(im.shape)
  for i in range(3):
    im2[:,:,i] = filters.gaussian_filter(im[:,:,i],args.sigma)
    # im2 = uint8(im2)

normalized_image = im/im2

if not args.blackwhite:
  normalized_image = normalized_image.astype('uint8')

figure()

if args.blackwhite:
  gray()

imshow(normalized_image)
axis('equal')
axis('off')

show()

