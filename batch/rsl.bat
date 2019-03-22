echo off

::IF %REDSHIFT_COREDATAPATH%==C:\ProgramData\Redshift (
::echo "Setting Path To SERVER"
::setx REDSHIFT_COREDATAPATH \\SERVER-CANOE\Canoe\Redshift
::) ELSE (
::echo "Setting Path To LOCAL"
::setx REDSHIFT_COREDATAPATH C:\ProgramData\Redshift
::)

set rspath=C:\ProgramData\Redshift
IF "%1"=="l" (set rspath=C:\ProgramData\Redshift)
IF "%1"=="s" (set rspath=\\SERVER-CANOE\Canoe\Redshift)

echo "Setting path to:"
echo %rspath%
setx REDSHIFT_COREDATAPATH %rspath%





