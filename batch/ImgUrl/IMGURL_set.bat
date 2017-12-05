set exif=%~dp0"exiftool.exe"

echo "Please enter your url"
set /p new_url="Enter URL: "
echo %new_url%
%exif% "-XMP:source=%new_url%" %1 -overwrite_original

::pause
