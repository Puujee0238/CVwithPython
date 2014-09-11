# line_detection.py
# find edges of objects using a Canny filter
# use case is to (eventually) identify individual agriculatural fields in satellite imagery

from PIL import Image
from numpy import *
from pylab import *
from scipy.ndimage import filters
from scipy.ndimage import measurements,morphology

# parameters
sigma_blur = 3	# scale for initial guassian blur (de-noising)
sigma_deriv = 2	# scale for gaussian filter for derivative
max_sup_size = 3	# size for footprint in filter for non-max gradient suppression
hyst_size = 3	# size for footprint in hystersis filter
threshold_low = 0.03	# low threshold for hysteresis filter
threshold_high = 0.1 # high threshold for hysteresis filter

class edge_filter_class:
	# To be used with ndimage.generic_filter

	def __init__(self,angles):
		self.angles = angles 	# matrix of gradient angles (same dimensions as image)
		self.coordinates = [0, 0]

	def filter_nonmax_suppress(self,bfr):
		# keep central pixel (at position 4 in buffer) if it's max, otherwise suppress
		# need to track current coordinate in the array to look up angle in self.angles
		gradient_vals = self.interpolated_gradients(bfr)
		# increment coordinates
		for jj in array([1, 0]):
			if self.coordinates[jj] < self.angles.shape[jj] - 1:
				self.coordinates[jj] += 1
				break
			else:
				self.coordinates[jj] = 0
		if bfr[4] > gradient_vals.max():
			return bfr[4]
		else:
			return 0

	def filter_hysteresis(self,bfr,t_low,t_high):
		# accept pixels above threshold_high; suppress pixels below threshold_low
		# intermediate pixels remain if connected to a pixel above threshold_high
		if bfr[4] > t_high:
			return 1
		elif bfr[4] < t_low:
			return 0
		elif bfr.max() > t_high:
			return 1
		else:
			return 0

	def interpolated_gradients(self,bfr):
		# get interpolated gradient values based on gradient direction/angle
		# conventions: x > 0 left, y > down, angle > 0 CW
		# pixel matrix reverses order because of abs() call
		angle = self.angles[self.coordinates[0],self.coordinates[1]]
		pixels = array([[0,0],[0,0]])

		if (angle >= 0 and angle < pi/4) or (angle >= -pi and angle < -3*pi/4):
			pixels = array([[bfr[5],bfr[8]],[bfr[0],bfr[3]]])
		elif (angle >= pi/4 and angle < pi/2) or (angle >= -3*pi/4 and angle < -pi/2):
			pixels = array([[bfr[7],bfr[8]],[bfr[0],bfr[1]]])
		elif (angle >= pi/2 and angle < 3*pi/4) or (angle >= -pi/2 and angle < -pi/4):
			pixels = array([[bfr[7],bfr[6]],[bfr[2],bfr[1]]])
		else: #(angle >= 3*pi/4 and angle <= pi) or (angle >= -pi/4 and angle < 0):
			pixels = array([[bfr[3],bfr[6]],[bfr[2],bfr[5]]])
		
		weight = ( abs(angle) % (pi/4) ) / (pi/4)
		weights = array([1-weight,weight])

		return dot(pixels,weights)

	def filter_find_thick_edges(self,bfr):
		# test whether edges are truly one pixel wide after non-max suppression
		# return 0 if edge is single-pixel-wde; 1 otherwise
		if bfr[4] == 0:	# not an edge
			return 0
		else:
			non_zeros = count_nonzero(bfr)
			if non_zeros > 5:	# 5 is max possible (a crossing) so this is thick
				return 1
			elif non_zeros < 4: # 1,2 must be thin; 3 is thin or a point
				return 0
			else:
				return 1 # stub out for now

	def filter_find_junctions(self,bfr):
		# test whether pixel is a junction of 2 or 3 edges
		# count number of edges encountered when circling around pixel
		if bfr[4] == 0: # not an edge
			return 0
		else:
			loop1 = array([bfr[0],bfr[1],bfr[2],bfr[5],bfr[8],bfr[7],bfr[6],bfr[3]])
			loop2 = array([bfr[1],bfr[2],bfr[5],bfr[8],bfr[7],bfr[6],bfr[3],bfr[0]])
			if (abs(loop1 - loop2)).sum() >= 6:
				return 1
			else:
				return 0

# Canny edge detection follows

# read image and smooth with gaussian blur
im0 = array(Image.open('data/merced.png'))
im1 = array(Image.open('data/merced.png').convert('L'))
im2 = filters.gaussian_filter(im1,sigma_blur)

# calculate derivatives/gradients
imx = zeros(im2.shape)
filters.gaussian_filter(im2,(sigma_deriv,sigma_deriv),(0,1),imx)
imy = zeros(im2.shape)
filters.gaussian_filter(im2,(sigma_deriv,sigma_deriv),(1,0),imy)
im3 = sqrt(imx**2+imy**2)
imangles = arctan2(imy,imx)

# suppress all but local max gradient
filter_class = edge_filter_class(imangles)
im4 = filters.generic_filter(im3,function=filter_class.filter_nonmax_suppress,size=max_sup_size)

# apply hysteresis threshold
t_low = threshold_low * im3.max()
t_high = threshold_high * im3.max()
im5 = filters.generic_filter(im4,function=filter_class.filter_hysteresis,size=hyst_size,extra_arguments=(t_low,t_high))

# save im5 for later
#f = open('fieldoutlines.pkl','wb')
#pickle.dump(im5,f)
#f.close()

# superimpose outlines on original image (boolean array)
im5bool = (im5 > 0)
im0[im5bool,:] = array([255,0,0])

# display
props = dict(boxstyle='round',facecolor='white')
fig=figure(figsize=(12,8))
axis('off')
#imshow(im0)
contour(im0,origin='image')
#text = 'Smoothing = %d \nDerivative = %d \nTL = %.2f \nTH = %.2f' % (sigma_blur,sigma_deriv,threshold_low,threshold_high)
#fig.text(0.05,0.95,text,transform=fig.transAxes,verticalalignment='top',bbox=props)
subplots_adjust(left=0,bottom=0,right=1,top=1,wspace=0,hspace=0)
show()