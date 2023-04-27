echo off
:: File path,  session, src_folder
::echo %1
::echo %2
::echo %3	

set out_dir=%3
set out_dir=%out_dir:Z:=./Fileserver/Projects%
::echo %1
::echo %out_dir%

winscp.com /ini=nul /command "open %2" "put -neweronly %1 %out_dir%/" "exit"

::pause

