#!/usr/bin/env python3
# coding: utf-8

___doc___ ="""{f}

thumb_scatter.py - making a scatter plot with thumbnail images

Usage:
	{f}	[-h|--help] [--scale=<scale>] [--emphasize=<class>] [--color] <input_csv_file> <plot_title> <output_file>

Options:
	--scale : size of thumnail (real number : default = 1.0)
	--emphasize : Class to be emphasize (4 digit hexadecimal code)
	--color : colorize character frames according to their colasses
	-h or --help : display this help message

""".format(f=__file__)

#	input_csv_file の形式
#		x座標, y座標, 画像ファイル
#	同じディレクトリの sample.csv を参照

from docopt import docopt
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
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
UseColor = False
Num = 60

def parse_options () :

	global InputCSV
	global PlotTitle
	global OutFile
	global Scale
	global EmpCode
	global UseColor

	args = docopt ( ___doc___ )

	InputCSV = args['<input_csv_file>']
	PlotTitle = args['<plot_title>']
	OutFile = args['<output_file>']
	
	if args['--scale']:
		Scale = float ( args['--scale'] )
		print ( 'scale = {}'.format(Scale))
	if args['--emphasize']:
		EmpCode = args['--emphasize']
		print ( 'pmphasize = {}'.format(EmpCode))
	if args['--color']:
		UseColor = True
		print ( 'color')

def frame_image(img, frame_width, value, cmap = None):

	b = frame_width # border size in pixel
	ny, nx = img.shape[0], img.shape[1] # resolution / number of pixels in x and y

	if img.ndim == 2: # grayscale image
		retm = np.empty((img.shape[0],img.shape[1],3),img.dtype)
		retm[:,:,:] = img[:,:,np.newaxis]
		img = retm

	framed_img = np.zeros((b+ny+b, b+nx+b, img.shape[2]))

	if cmap != None :
		framed_img[:,:] = np.asarray(cmap.jet(value))[0:3]

	framed_img[b:-b, b:-b] = img
	return framed_img


def get_class ( fname ):
	import os
	basename = os.path.basename(fname)
	ret = basename.split('_')[0]
	return ret

		
def scatter_image(feature_x, feature_y, image_paths, title, save=None, code_list=None):
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

		if EmpCode != "" and get_class ( path ) == EmpCode :
			img = frame_image ( img, 30, 0 )
			
		elif code_list != None :
			idx = code_list.index ( get_class (path) )
			img = frame_image ( img, 30, float(idx) / len(code_list), cmap=cm )

		disp_size = max ( xlim[1]-xlim[0], ylim[1]-ylim[0] ) / Num
		bb = Bbox.from_bounds(x, y, disp_size*Scale, disp_size * Scale)
		bb2 = TransformedBbox(bb, ax.transData)
		bbox_image = BboxImage(bb2, cmap=None, norm=None, origin=None, clip_on=False)
			
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
	code_list = list()
	with open (InputCSV, 'r') as fin :
		reader = csv.reader(fin)
		for row in reader :
			X.append ( row[0] )
			Y.append ( row[1] )
			images.append ( row[2] )
			code = get_class ( row[2] )
			if (code in code_list) == False : 
				code_list.append(code)

	featX = np.array(X, dtype=float)
	featY = np.array(Y, dtype=float)

	if UseColor == True:
		code_list.sort()
		scatter_image ( featX, featY, images, PlotTitle, code_list = code_list, save = OutFile )
	else:
		scatter_image ( featX, featY, images, PlotTitle, save = OutFile )
