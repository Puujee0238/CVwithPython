import os
from PIL import *
from numpy import *
from pylab import *

def get_imlist(path):
	"""Returns a list of filenames for all jpg images in a directory."""
	return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]

def imresize(im,sz):
	"""Resize and image array using PIL."""
	pil_im = Image.fromarray(uint8(im))
	return array(pil_im.resize(sz))

def histeq(im,nbr_bins=256):
	"""Histogram equalization of a grayscale image."""
	# get image histogram
	imhist,bins = histogram(im.flatten(),nbr_bins,normed=True)
	cdf = imhist.cumsum() # cumulative distribution function
	cdf = 255 * cdf / cdf[-1] # normalize
	# use linear interpolation of cdf to find new pixel values
	im2 = interp(im.flatten(),bins[:-1],cdf)
	return im2.reshape(im.shape), cdf

def compute_average(imlist):
	"""Compute the average of list of images."""
	# open first image and make into an array of type float
	averageim = array(Image.open(imlist[0]),'f')
	for imname in imlist[1]:
		try:
			averageim += array(Image.open(imname))
		except:
			print imname + '...skipped'
	averageim /= len(imlist)
	#return average as uint8
	return array(averageim,'uint8')

def pca(X):
	""" Principal Component anlaysis
		input: X, matrix with training data stored as flattened arrays in rows
		return: projection matrix (with big dimensions first), variance and mean"""
	# get dimensions
	num_data,dim = X.shape
	# center data values
	mean_X = X.mean(axis=0)
	X = X - mean_X
	if dim > num_data:
		# PCA - compact trick used
		M = dot(X,X.T) # covariance matrix
		e,EV = linagl.eigh(M) # eigenvalues and eigenvectors
		tmp = dot(X.T,EV).T # compact trick
		V = tmp[::-1] #reverse since last eigenvectors are what we want
		S = sqrt(e)[::-1] # reverse since evals are in increasing order
		for i in range(V.shape[1]):
			V[:,i] /= S
	else:
		# PCA - SVD used
		U,S,V = linalg.svd(X)
		V = V[:num_dat] # only makese sense to return first num_dat
	# return projection matrix, variance, mean
	return V,S,mean_X

def denoise(im,U_int,tolerance=0.1,tau=0.125,tv_weight=100):
	"""An implementation of the Rudin-Osher-Fatemi (ROF) denoising model
	using the numerical procedure in eqn 11 from A. Chambolle (2005)
	Input: noisy input image (grayscale), initial guess for U, weight of
	the TV-regularizing term, steplength, tolerance for stop criterion.
	Output: denoise and detextured image, texture residual."""

	m,n = im.shape #size of image
	#initialize
	U = U_init
	Px = im #x component of dual field
	Py = im #y component
	error = 1
	while (error > tolerance):
		Uold = U
		#gradient of primal variable
		GradUx = roll(U,-1,axis=1)-U #x component of U's gradient
		GradUy = roll(U,-1,axis=0)-U #y component
		#update dual variable
		PxNew = Px + (tau/tv_weight)*GradUx
		PyNew = Py + (tau/tv_weight)*GradUy
		NormNew = maximum(1,sqrt(PxNew**2+PyNew**2))
		Px = PxNew/NormNew
		Py = PyNew/NormNew
		#update primal
		RxPx = roll(Px,1,axis=1)
		RyPy = roll(Py,1,axis=0)
		DivP = (Px-RxPx)+(Py-RyPy)
		U = im+tv_weight*DivP
		# update error
		error = linalg.norm(U-Uold)/sqrt(n*m)
	return U,im-U




