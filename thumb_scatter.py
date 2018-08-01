#!/usr/bin/env python3
# coding: utf-8

___doc___ ="""{f}

thumb_scatter.py - making a scatter plot with thumbnail images

Usage:
	{f}	[-h|--help] [--scale=<scale>] [--emphasize=<class>] <input_csv_file> <plot_title> <output_file>

Options:
	--scale : size of thumnail (real number : default = 1.0)
	--emphasize : Class to be emphasize (4 digit hexadecimal code)
	-h or --help : display this help message

""".format(f=__file__)

#	input_csv_file の形式
#		x座標, y座標, 画像ファイル
#	同じディレクトリの sample.csv を参照

from docopt import docopt
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.image import BboxImage
from matplotlib.transforms import Bbox, TransformedBbox
import numpy as np
import csv
import sys

## =======================================
#	Global variables
## =======================================

InputCSV=''
PlotTitle=''
OutFile=''
Scale = 1.0
EmpCode = ''

Num = 60

def parse_options () :

	global InputCSV
	global PlotTitle
	global OutFile
	global Scale
	global EmpCode

	args = docopt ( ___doc___ )

	InputCSV = args['<input_csv_file>']
	PlotTitle = args['<plot_title>']
	OutFile = args['<output_file>']
	
	if args['--scale']:
		Scale = float ( args['--scale'] )
		print ( 'scale = {}'.format(Scale))
	if args['--emphasize']:
		EmpCode = args['--emphasize']
		print ( 'scale = {}'.format(Scale))


def frame_image(img, frame_width):
	b = frame_width # border size in pixel
	ny, nx = img.shape[0], img.shape[1] # resolution / number of pixels in x and y
	if img.ndim == 3: # rgb or rgba array
		framed_img = np.zeros((b+ny+b, b+nx+b, img.shape[2]))
	elif img.ndim == 2: # grayscale image
		framed_img = np.zeros((b+ny+b, b+nx+b))
	framed_img[b:-b, b:-b] = img
	return framed_img


def get_class ( fname ):
	import os
	basename = os.path.basename(fname)
	ret = basename.split('_')[0]
	return ret

		
def scatter_image(feature_x, feature_y, image_paths, title, save=None):
	"""
	Args:
	feature_x: x座標
	feature_y: y座標
	image_paths: 
	"""
	global Scale

	fig = plt.figure()
	ax = fig.add_subplot(111)
	xlim = [np.min(feature_x)-5, np.max(feature_x)+5]
	ylim = [feature_y.min()-5, feature_y.max()+5]

	for (x, y, path) in zip(feature_x, feature_y, image_paths):
		img = plt.imread(path)

		disp_size = max ( xlim[1]-xlim[0], ylim[1]-ylim[0] ) / Num
		bb = Bbox.from_bounds(x, y, disp_size*Scale, disp_size * Scale)
		bb2 = TransformedBbox(bb, ax.transData)
		bbox_image = BboxImage(bb2, norm=None, origin=None, clip_on=False)

		if EmpCode != "" and get_class ( path ) == EmpCode :
			print ( "{}".format (EmpCode) )
			img = frame_image ( img, 15 )

		bbox_image.set_data(img)
		ax.add_artist(bbox_image)
	ax.set_ylim(*ylim)
	ax.set_xlim(*xlim)
	plt.title(title)
	if save is not None:
		plt.savefig(save, dpi=600)
	plt.show()


if __name__ == '__main__':

	parse_options ()

	X = []
	Y = []
	images = []
	
	with open (InputCSV, 'r') as fin :
		reader = csv.reader(fin)
		for row in reader :
			X.append ( row[0] )
			Y.append ( row[1] )
			images.append ( row[2] )

	featX = np.array(X, dtype=float)
	featY = np.array(Y, dtype=float)

	scatter_image ( featX, featY, images, PlotTitle, save = OutFile )
