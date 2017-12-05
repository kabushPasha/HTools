echo off
set exif=%~dp0"exiftool.exe"

echo Processing image %*

::echo "Please enter your url"
set /p new_url="Enter URL: "
::echo %new_url%
%exif% "-XMP:source=%new_url%" "%*" -overwrite_original

set /p new_name="Enter Link Name: "
::echo %new_name%
ren "%*" "%new_name%"

pause
