::"S:\HTools\batch\FTP\download.bat" ! !/

echo off

::echo %1
::echo %~nx2
::echo %~dp2


set str=%2
::echo %str%
set str=%str:/Fileserver/Projects/=Z:/%

robocopy /S /E %~dp1 %str% *
::pause
