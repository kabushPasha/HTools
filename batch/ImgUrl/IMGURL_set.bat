:: add auto add extension
:: add auto move to folder

echo off
set exif=%~dp0"exiftool.exe"

echo Processing image %1

::echo "Please enter your url"
set /p new_url="Enter URL: "
%exif% "-XMP:source=%new_url%" %1 -overwrite_original

set /p new_name="Enter Link Name: "
if "%new_name%"=="" (
	echo "i'll keep my name"
) else (
	ren %1 "%new_name%"
)

set /p new_folder="Enter Folder Name: "

if "%new_folder%"=="" (
echo "I'll stay here"
) else (
echo move me to %new_folder%
echo %cd%\%new_folder%
ROBOCOPY "%cd%" "%cd%\%new_folder%" "%new_name%" /mov /NFL /NDL /NJH /NJS
)

pause
