echo off
:: File path,  session, src_folder
::echo %1
::echo %2
::echo %3	

set out_dir=%3
set out_dir=%out_dir:/Fileserver/Projects=Z:%
::echo %1
::echo %out_dir%

winscp.com /ini=nul /command "open %2" "cd %3" "get -neweronly %1 %out_dir%\" "exit"

::pause

