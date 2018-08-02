#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#	rank_images.py -- Creating ranking image list
#
#	Usage: python3 rank_images.py InputFile(.csv)
#

import subprocess
import csv
import sys
import numpy as np

args = sys.argv
InputCSV = args[1]
OutputPNG = InputCSV.replace ('.csv', '')

cnv_options = " -resize 128x128 -gravity center -background 'rgb(255,255,255)' -extent 128x128 -bordercolor 'rgb({})' -border 2x2 "


def get_class ( fname ):
	import os
	
	basename = os.path.basename(fname)
	ret = basename.split('_')[0]
	return ret

num = 0

with open( InputCSV, 'rt' ) as fin:
	cin = csv.reader(fin)

	rank_num = 0
	q_class = ""
	cmd = "convert "


	for line in cin:

		#### ブロックの切れ目：コマンドを発行して，次のクエリを読み込む
		if line == ['\n'] :
			cmd += " +append tmp.png"
			subprocess.run(cmd,shell=True)

			if num % 10 == 0 :
			 	subprocess.call ( "convert tmp.png {}_{:03}.png".format(OutputPNG,num//10), shell=True )
			else:
			 	subprocess.call ( "convert {}_{:03}.png tmp.png -append {}_{:03}.png".format(OutputPNG,num//10,OutputPNG,num//10), shell=True )
			num = num+1

			rank_num = 0
			cmd = "convert "

		#### クエリ画像
		elif len(line) == 1 :
			sub_cmd = "convert " +line[0] + cnv_options.format("0,0,255") + " -gravity northwest -extent 138x134 query.png"
			subprocess.run(sub_cmd, shell=True)
			q_class = get_class ( line[0] )
			print ( "query: {}".format(line[0]) )

			cmd += "query.png "

		#### ランキング画像
		else:
			r_class = get_class ( line[0] )
			
			if q_class == r_class : 
				col = "0,0,255"
			else:
				col = "255,0,0"

			sub_cmd = "convert " +line[0] + cnv_options.format(col) + " rank_{}.png".format(rank_num)
			subprocess.run(sub_cmd, shell=True)

			cmd += "rank_{}.png ".format(rank_num)
			rank_num += 1
