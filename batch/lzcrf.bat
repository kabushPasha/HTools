set file=%1
set crf= %2

IF "%2"=="" set crf=10

ffmpeg -i %1 -c:v libx264 -pix_fmt yuv420p -preset veryslow -crf %crf%  -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" "out.mp4"