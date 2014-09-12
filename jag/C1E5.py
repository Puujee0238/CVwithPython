# Use gradient direction and magnitude to detect lines in an image. Estimate
# the extent of the lines and their parameters. Plot the lines overlaid on the
# image.

import argparse
from PIL import Image
from numpy import array, zeros, uint8, sqrt, arctan2
from pylab import imshow, show, gray, figure, contour, axis
from scipy.ndimage import filters
import math
from collections import defaultdict


parser = argparse.ArgumentParser(description='Apply unsharp filter.')
parser.add_argument('sigma', metavar='sigma', type=int, default=1,
                   nargs='?', help='Sigma for gaussian blue')
parser.add_argument('scale', metavar='scale', type=float, default=0.1,
                   nargs='?', help='scale for gaussian subtraction')

args = parser.parse_args()

raw_image = Image.open('data/detect_lines1.png').convert('L')
im = array(raw_image)
nx, ny = im.shape
print im.shape, im.dtype

#Threshhold for our gradient magnitude
threshhold = 0.2
# minimum number of points for a 'line'
minpoints = 5

#Sobel derivative filters
Dx = zeros(im.shape)
filters.sobel(im,1,Dx)
Dy = zeros(im.shape)
filters.sobel(im,0,Dy)
Dmag = sqrt(Dx**2+Dy**2)
Dang = arctan2(Dx,Dy)
Dthresh = (Dmag > threshhold)


# Scan L to R, finding lines
# Lines are arrays of points, all with the same angle and contiguous

# we identify lines by their angle and top-left intersect.
# XXX: This will equate "colinear lines"
# We can post-process to separate these.
# We will also discard all lines < 5 pixels in length

# Given a point and its derivative, find the x-intersect.
# (For horizontal lines, return the y-intersect)
def findIntersect(p, d):
  x, y = p
  dx, dy = d
  if dy == 0: return y
  return math.floor(x - 1.0*dx*y/dy)

def findKey(p, d, theta):
  intersect = findIntersect(p, d)
  return "%s_%s" % (theta, intersect)

lines = defaultdict(list)

for x in range(nx):
  for y in range(ny):
    if Dmag[x,y] < threshhold: continue
    lineKey = findKey( (x, y), (Dx[x,y], Dy[x, y]), Dang[x, y] )
    lines[lineKey].append((x,y))

lines = { k:l for (k, l) in lines.items() if len(l) >= minpoints}

[line.sort() for line in lines.values()]


# processed_lines = []
# for line in processed_lines:
#   new_line = []
#   lastpoint = None
#   for (x,y) in line:
#
#     if (lastpoint == None)\
#       or (math.abs(lastpoint[0] - x) <= 1)\
#       or (math.abs(lastpoint[1] - y) <= 1):
#          #contiguous point
#          new_line.append((x,y))
#          lastpoint = (x,y)
#     else:
#       processed_lines.append(new_line)
#       new_line = [(x,y)]
#       lastpoint = (x,y)
#   processed_lines.append(new_line)
#
# processed_lines = [line for line in processed_lines if len(line) >= minpoints]

# Now let's plot them
line_img = zeros(im.shape)

for line in lines.values():
  for (x,y) in line:
    line_img[x,y] = 1.0

figure()
gray()
imshow(line_img)
show()
