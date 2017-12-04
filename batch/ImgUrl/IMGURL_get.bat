set exif=%~dp0"exiftool.exe"

for /f %%i in ('%exif% -s -s -s -XMP:source %1') do set RESULT=%%i
start %RESULT%




