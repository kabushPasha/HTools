@echo off
mkdir "converted"
for %%F in (*.mp4) do (
    ffmpeg -i "%%F" -vf "scale=1920:1080" -c:v libx264 -crf 23 -preset slow -profile:v high -level 4.0 -pix_fmt yuv420p -c:a copy "converted\%%~nF_converted.mp4"
)
pause