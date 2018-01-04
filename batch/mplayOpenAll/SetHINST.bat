Rem set Houdinitools environment variable to current folder
set "dir=%~dp0"
setx HINST "%dir:~0,-1%"
pause