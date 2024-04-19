mkdir out_jpg
magick mogrify -verbose -format jpg -quality 90% -path ./out_jpg/ *.png