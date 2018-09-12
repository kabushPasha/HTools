set name=%~n0.ps1
set name=%name:CreateShortcut=%
powershell -File %name% -cs
::pause