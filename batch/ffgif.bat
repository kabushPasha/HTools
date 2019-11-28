set filename=%~n1
set res=%2

IF "%2"=="" set res=-1

ffmpeg -i %1 -vf "fps=24,scale=%res%:-1:flags=lanczos,palettegen" -y temp_gif_palette.png
ffmpeg -i %1 -i temp_gif_palette.png -lavfi "fps=24,scale=%res%:-1:flags=lanczos [x]; [x][1:v] paletteuse" -y "%filename%.gif"

del temp_gif_palette.png
