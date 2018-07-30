# thumbnails_scatter
Creating a 2D scatter plot with thumbnail images

# Basic usage
    $ python3 ./thumb_scatter.py --help
    thumb_scatter.py - making a scatter plot with thumbnail images
    
    Usage:
      thumb_scatter.py	[-h|--help] [--scale=scale_value] input_csv_file plot_title output_file
    
    Options:
      --scale : size of thumnail (scale value as a real number : default = 1.0)
      -h or --help : display this help message

# Format of input CSV file
The input CSV file contains one sample par one line in the following format.  
''' x, y, image file name '''  
Please see `sample.csv`.

    2.35,1.89,sample_imgs/a001.png
    4.59,-2.08,sample_imgs/a002.png
    -3.2,-0.0116,sample_imgs/a003.png
    -1.24,3.64,sample_imgs/a004.png
    -1.02,-0.0455,sample_imgs/a005.png

# Sample

    python3 ./thumb_scatter.py -scale=1.8 sample.csv 'sample scatter plot' sample.pdf

![sample image](https://github.com/uchidalab/thumbnails_scatter/blob/master/sample.png "サンプル")

# Others
If sample number in the CSV is too may to see the result. You can reduce the number by the following command.

    awk 'NR%2==0{print $0}' sample.csv > re_sample.csv

The command output only even samples, so the number of samples is reduced as 1/2.
