set file=%1
set crf= %2

IF "%2"=="" set crf=10

ffmpeg -i %1 -c:v libx264 -preset veryslow -crf %crf% "out.mp4"