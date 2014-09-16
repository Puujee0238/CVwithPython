import argparse
from PIL import Image
from numpy import array, zeros, ones, uint8, histogram
from pylab import imshow, show, gray, figure, axis, hist
from scipy.ndimage import measurements, morphology


parser = argparse.ArgumentParser(description='Plot distribution of object size (in pixels)')
parser.add_argument('filename', type=str, help='Path to image.')

args = parser.parse_args()

im = array(Image.open(args.filename).convert('L'))
im = 1*(im<128)

im_open = morphology.binary_opening(im,ones((9,5)),iterations=2)

labels, n_objs = measurements.label(im_open)
max_label = labels.max()
sizes = []
for i in range(max_label+1):
  sizes.append( sum(labels.flatten() == i) )

# The 0 label is the background; ignore it.
sizes.pop(0);

figure()
# hist(labels.flatten(), bins=max_label, range=(1, max_label+1))
hist(sizes)
# gray()
show()
