# C1E8-pca-compression.py
# use PCA on corpus of images of lower-case "a" in different fonts
# determine principal components, then compress all images using these
# decompress images and display
# results: decent reconstruction when using >~ 250 modes (out of 625)
# problem with normalization (don't understand yet)

from PIL import Image
from numpy import *
from pylab import *
import os

# parameters
num_modes_to_use = 625		# number of pca components to use in compression
num_reconstructed_im_display = 15	# num of reconstructed images to display at end

def get_imlist(path):
	return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]

def pca(X):
	num_data,dim = X.shape			# get dimensions
	mean_X = X.mean(axis=0)	
	X = X - mean_X							# center data
	if dim > num_data:
		M = dot(X,X.T)						# covariance matrix
		e,EV = linalg.eigh(M)			# evals and evectors
		tmp = dot(X.T,EV).T 			# compact trick (?)
		V = tmp[::-1]							# reverse to get last evectors
		S = sqrt(e)[::-1]					# reverse because evals are in increasing order
		for i in range(V.shape[1]):
			V[:,i] /= S
	else:
		U,S,V = linalg.svd(X)
		V = V[:num_data]
	return V,S,mean_X

# begin main

imlist = get_imlist('data/a_thumbs/')
im = array(Image.open(imlist[0]))			
m,n = im.shape[0:2]									# get size of each image
imnbr = len(imlist)									# number of images in corpus

# make matrix to store all flattened images
immatrix = array([array(Image.open(im)).flatten() for im in imlist],'f')

# do pca
V,S,immean = pca(immatrix)

# calculate 'projection' of each image into components/modes
projections = zeros((imnbr,num_modes_to_use))
for jj in range(num_modes_to_use):
	projections[:,jj] = dot(immatrix,V[jj])

# calculate 'reconstruction' from projections
immatrix_R = outer(ones(imnbr),immean)			# start with the mean
for jj in range(num_modes_to_use):
	immatrix_R += outer(projections[:,jj],V[jj])	# add each mode per its projection weight

# renormalize reconstruction
r_max = immatrix_R.max()
r_min = immatrix_R.min()
scale_factor = (255 - 0) / (r_max - r_min)
immatrix_R = uint8(scale_factor * (immatrix_R - r_min))

# display cumulative eigenvalues by mode (gives sense of modes needed for compression)
#S_cumulative = cumsum(S)/(S.sum())
#figure()
#gray()
#N = range(len(S_cumulative))
#plot(N,S_cumulative)
#title('Cumulative eigenvals of principal components (625 total)')
#show()

# display a few original and reconstructed images
figure(figsize=(16,2))
gray()
for jj in range(num_reconstructed_im_display):
	subplot(2,num_reconstructed_im_display,jj+1)
	axis('off')
	imshow(immatrix[jj].reshape(m,n))
	subplot(2,num_reconstructed_im_display,jj+num_reconstructed_im_display+1)
	axis('off')
	imshow(immatrix_R[jj].reshape(m,n))
subplots_adjust(left=0,bottom=0,right=1,top=1,wspace=0,hspace=0)
show()