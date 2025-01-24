set HU_PATH=D:\ML\Hun3dV2\Hunyuan3D2_WinPortable



@REM Set the correct path for CUDA Toolkit if you install it elsewhere.
set CUDA_HOME=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.4


@REM ===========================================================================
@REM These settings usually don't need change.

@REM This command redirects HuggingFace-Hub to download model files in this folder.

set HF_HUB_CACHE=%HU_PATH%\HuggingFaceHub


@REM This command will set PATH environment variable.
set PATH=%PATH%;%HU_PATH%\python_standalone\Scripts
set PATH=%PATH%;%CUDA_HOME%\bin

@REM This command will let the .pyc files to be stored in one place.
set PYTHONPYCACHEPREFIX=%HU_PATH%\pycache

:: Set current DIR
set SRC_DIR=%cd%


@REM ===========================================================================

cd /D %HU_PATH%\Hunyuan3D-2

..\python_standalone\python.exe -s hu3d_folder.py

pause
