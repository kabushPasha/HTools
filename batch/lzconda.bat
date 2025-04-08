@echo off
REM Change 'myenv' to your actual Conda environment name
set ENV_NAME=myenv

REM Optional: Set path to your Anaconda installation if needed
REM Replace with your Anaconda install path if not already in PATH
set "CONDA_PATH=D:\Soft\Conda"
call "%CONDA_PATH%\Scripts\activate.bat"

REM Activate Conda environment
REM call conda activate %ENV_NAME%

timeout /t 2 > nul

set LAUNCH_JUPYTER=false
for %%A in (%*) do (
    if "%%A"=="-j" set LAUNCH_JUPYTER=true
)

if "%LAUNCH_JUPYTER%"=="true" (
    call jupyter notebook
)



REM Keep the CMD window open
cmd /K