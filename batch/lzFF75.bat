echo off

:: Get Startframe
:: if start frame is not provided it will be set to 1
set startframe=%1
IF "%1"=="" set startframe=1
::echo %startframe%

:: Get Current Directory
for %%I in (.) do set CurrDirName=%%~nxI
echo %CurrDirName%

:: Convert Frames To Video
ffmpeg -start_number %startframe% -framerate 75 -i %%04d.jpg -c:v libx264  -pix_fmt yuv420p -preset veryslow -crf 0 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -r 75 "%cd%.mp4"

:: Convert Video to a better format
cd .. 
lzcrf %CurrDirName%.mp4


