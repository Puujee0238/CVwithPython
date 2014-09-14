import argparse
from PIL import Image
from numpy import array, zeros, empty, ones, uint8, histogram
from pylab import imshow, show, gray, figure, axis, hist
from scipy.ndimage import measurements, morphology


parser = argparse.ArgumentParser(description='Plot distribution of object size (in pixels)')
parser.add_argument('filename', type=str, help='Path to image.')
parser.add_argument('--structureX', '-x', dest='x', type=int, default=5,
  help='X size of structuring element.')
parser.add_argument('--structureY', '-y', dest='y', type=int, default=9,
  help='Y size of structuring element.')
parser.add_argument('--iterations', '-i', type=int, default=2,
  help='Number of opening iterations to perform.')
parser.add_argument('--threshhold', '-t', type=int, default=128,
  help='Greyscale threshhold to make binary image.')



args = parser.parse_args()

im = array(Image.open(args.filename).convert('L'))
im = 1*(im<args.threshhold)

im_open = morphology.binary_opening(im,ones((args.y,args.x)),iterations=args.iterations)

figure()
gray()

labels, n_objs = measurements.label(im_open)

com = measurements.center_of_mass(im_open, labels, range(1, n_objs))
# print com

for (xx, yy) in com:
  x = int(xx + 0.5)
  y = int(yy + 0.5)
  im_open[x, y] = 255
  for i in (1, -1):
    im_open[x+i, y] = 0
    im_open[x, y+i] = 0

imshow(im_open)
show()
