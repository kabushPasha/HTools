set exif=%~dp0"exiftool.exe"
set file="%*"
for /f %%i in ('%exif% -s -s -s -XMP:source %file%') do set RESULT=%%i
explorer "%RESULT%"

::pause
