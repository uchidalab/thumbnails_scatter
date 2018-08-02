# thumbnails_scatter
Creating a 2D scatter plot with thumbnail images

## Basic usage
    $ python3 ./thumb_scatter.py --help
    thumb_scatter.py - making a scatter plot with thumbnail images
    
    Usage:
      thumb_scatter.py	[-h|--help] [--scale=scale_value] input_csv_file plot_title output_file
    
    Options:
      --scale : size of thumnail (scale value as a real number : default = 1.0)
			--emphasize : Class to be emphasize (4 digit hexadecimal code)
      -h or --help : display this help message

## Format of input CSV file
The input CSV file contains one sample par one line in the following format.  
''' x, y, image file name '''  
Please see `sample.csv`.

    2.35,1.89,sample_imgs/a001.png
    4.59,-2.08,sample_imgs/a002.png
    -3.2,-0.0116,sample_imgs/a003.png
    -1.24,3.64,sample_imgs/a004.png
    -1.02,-0.0455,sample_imgs/a005.png

## Sample

    python3 ./thumb_scatter.py -scale=1.8 sample.csv 'sample scatter plot' sample.pdf

![sample image](https://github.com/uchidalab/thumbnails_scatter/blob/master/sample.png "サンプル")

## Others
If sample number in the CSV is too may to see the result. You can reduce the number by the following command.

    awk 'NR%2==0{print $0}' sample.csv > re_sample.csv

The command output only even samples, so the number of samples is reduced as 1/2.


# Ranking image list generation
Creating ranking list image

## Basic usage

    $ python3 ./rank_images.py Input_CSV_File

## Format of input CSV file
The input CSV file contains multiple data blocks.
One data block consits of multiple lines.

    <filename of query image>
    <filename of rank-n image>,<distance value> (repeated n-times)
    "
    " (delimiter of image block)

Example:

    resize/0812_0614086.png
    resize/0813_0614087.png,26.48101234436035
    resize/1108_0622215.png,29.828632354736328
    resize/1748_0625685.png,30.70377540588379
    resize/0635_0610158.png,32.40945053100586
    resize/0022_0601027.png,33.12775421142578
    "
    "
    resize/1520_0625400.png
    resize/1435_0625299.png,30.205413818359375
    resize/0208_0622363.png,32.262229919433594
    resize/0240_0604146.png,32.40801239013672
    resize/1476_0625349.png,33.261756896972656
    resize/0560_0610020.png,33.75419616699219
    "

## Sample

```python3 ./rank_images.py ./Img_Dist/cae_L2.csv```

![sample image](https://github.com/uchidalab/thumbnails_scatter/blob/master/cae_L2_000.png "サンプル")

*NOTE* The program outputs result images in the directory where the CSV file is.
