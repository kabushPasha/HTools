::echo "Hi"
::echo %1

set str=%1
set str=%str:/Fileserver/Projects/=Z:/% 

ECHO | SET /P=%str% | CLIP

