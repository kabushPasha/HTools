echo off
cd ..
set maya="C:\Program Files\Autodesk\Maya2017\bin\maya.exe"

:: get scene path
set "scenePath=%1"
set "scenePath=%scenePath:\=/%"

:: Maya simply loaded abc plugins after the scene,so we load the plugin first here

::set command=loadPlugin "AbcExport";loadPlugin "AbcImport";file -f -loadReferenceDepth \"all\" -open \"%scenePath%\";
set command=loadPlugin "AbcExport";loadPlugin "AbcImport";file -f -open \"%scenePath%\";
::echo "%command%"

start "" %maya% -command "%command%"  -proj %cd%









:: Older version, might still be good if user sets ABC plugins to load before scene
::cd ..
::set maya="C:\Program Files\Autodesk\Maya2017\bin\maya.exe"
::start "Maya" %maya% -file %1 -proj %cd%
