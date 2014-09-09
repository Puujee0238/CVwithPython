# harris.py

from PIL import Image
from numpy import *
import matplotlib.pyplot as pyplot
from scipy.ndimage import filters
from scipy.ndimage import measurements,morphology
import imtools

def compute_harris_response(im,sigma=3):
	"""Compute Harris corner detector response"""

	# derivatives
	imx = zeros(im.shape)
	filters.gaussian_filter(im,(sigma,sigma),(0,1),imx)
	imy = zeros(im.shape)
	filters.gaussian_filter(im,(sigma,sigma),(1,0),imy)

	# components
	Wxx = filters.gaussian_filter(imx*imx,sigma)
	Wyy = filters.gaussian_filter(imy*imy,sigma)
	Wxy = filters.gaussian_filter(imx*imy,sigma)

	# determinant and trace; include small epsilon to avoid Wtr = 0
	Wdet = Wxx*Wyy - Wxy**2
	Wtr = Wxx + Wyy + 0.001

	if Wtr.min() == 0:
		print 'Divide by zero'

	return Wdet / Wtr

def get_harris_points(harrisim,min_dist=10,threshold=0.1):
	"""Identify and sort candidate corner points; 
	filter out ones that are too close"""

	# find top corner candidates above a threshold
	corner_threshold = harrisim.max() * threshold
	harrisim_t = (harrisim > corner_threshold) * 1

	# get coords, vals of candidates; sort
	ccoords = array(harrisim_t.nonzero()).T
	cvals = [harrisim[c[0],c[1]] for c in ccoords]
	index = argsort(cvals)

	# store allowed points in an array (away from edge)
	allowed_locations = zeros(harrisim.shape)
	allowed_locations[min_dist:-min_dist,min_dist:-min_dist] = 1

	# identify best corner candidates, separated by min_dist
	filtered_candidates = []
	for i in index:
		cx = ccoords[i,0]
		cy = ccoords[i,1]
		if allowed_locations[cx,cy] == 1:
			filtered_candidates.append(ccoords[i])
			allowed_locations[(cx-min_dist):(cx+min_dist),(cy-min_dist):(cy+min_dist)] = 0

	return filtered_candidates

def plot_harris_points(im,filtered_candidates):
	"""Plot corners found in image"""

	pyplot.figure()
	pyplot.gray()
	pyplot.imshow(im)
	pyplot.plot([p[1] for p in filtered_candidates],[p[0] for p in filtered_candidates],'r*')
	pyplot.axis('off')
	pyplot.show()
