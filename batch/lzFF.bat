::ffmpeg -i %%04d.jpg -c:v libx264 -preset veryslow -crf 0 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" ../output.mp4
ffmpeg -i %%04d.jpg -c:v libx264 -preset veryslow -crf 0 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" "%cd%.mp4"
.mp4