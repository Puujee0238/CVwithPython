import argparse
from PIL import Image
from numpy import array
from pylab import show, gray, figure

# Python sure does make it hard to include a module from the dir above...
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import harris

'''
1. Modify the function for matching Harris corner points to also take a maximum
pixel distance between points for them to be considered as correspondences in
order to make matching more robust.
'''

parser = argparse.ArgumentParser(description='Find corresponding corners with harris detector.')
parser.add_argument('filename1', type=str, help='Path to first image.')
parser.add_argument('filename2', type=str, help='Path to second image.')
parser.add_argument('--maxdist', '-m', dest='maxdist', type=int,
  help='If set, restrict matches to be within maxdist.')
parser.add_argument('--width', '-w', dest='width', type=int, default=5,
  help='Width of descriptors.')
parser.add_argument('--sigma', '-s', dest='sigma', type=int, default=5,
  help='Sigma for gaussian blurring.')

args = parser.parse_args()

wid = args.width

im1 = array(Image.open(args.filename1).convert('L'))
harrisim = harris.compute_harris_response(im1,args.sigma)
filtered_coords1 = harris.get_harris_points(harrisim,wid+1)
d1 = harris.get_descriptors(im1,filtered_coords1,wid)

im2 = array(Image.open(args.filename2).convert('L'))
harrisim = harris.compute_harris_response(im2,args.sigma)
filtered_coords2 = harris.get_harris_points(harrisim,wid+1)
d2 = harris.get_descriptors(im2,filtered_coords2,wid)

print 'starting matching'
matches = harris.match_twosided(d1,d2)

figure()
gray()
harris.plot_matches(im1,im2,filtered_coords1,filtered_coords2,matches)
show()
