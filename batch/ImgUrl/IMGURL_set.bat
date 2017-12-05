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
	ren %1 "%new_name%"%~x1
)

::ECHO filedrive=%~d1
::ECHO filepath=%~p1
::ECHO filename=%~n1
::ECHO fileextension=%~x1

set dir=%~d1%~p1
set /p new_folder="Enter Folder Name: "

:: bug will move nothing if new name not set
if "%new_folder%"=="" (
echo "I'll stay here"
) else (
echo "I'll go away"
Robocopy.exe  "%dir%." "%dir%%new_folder%" "%new_name%%~x1" /mov /NFL /NDL /NJH /NJS
)
pause
