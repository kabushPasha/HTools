::ffmpeg -i %%04d.jpg -c:v libx264 -preset veryslow -crf 0 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" ../output.mp4

:: if start frame is not provided it will be set to 1

set startframe=%1
IF "%1"=="" set startframe=1
::echo %startframe%

ffmpeg -start_number %startframe% -framerate 24 -i %%04d.jpg -c:v libx264  -pix_fmt yuv420p -preset veryslow -crf 0 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -r 24 "%cd%.mp4"
