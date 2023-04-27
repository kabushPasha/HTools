::echo "Hi"
echo %1

set str=%1
set str=%str:Z:\=/Fileserver/Projects/% 
set str=%str:\=/%

ECHO | SET /P=%str% | CLIP
