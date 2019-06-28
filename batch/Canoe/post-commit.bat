SET REPOS=%1
SET REV=%2
SET TXN_NAME=%3

:: Manually Enter Path
::SET REPOS="S:\Ramona"
::"C:\\Program Files\\TortoiseSVN\\bin\\svn.exe" update %REPOS% --quiet --non-interactive --username RenderFarmer --password 1111

:: Auto Find Path
cd /d %REPOS%
set path1=%cd%
cd ..
set path2=%cd%
call set "path3=%%path1:%path2%\=%%"
"C:\\Program Files\\TortoiseSVN\\bin\\svn.exe" update S:\%path3% --quiet --non-interactive --username Server --password fightclub1999


