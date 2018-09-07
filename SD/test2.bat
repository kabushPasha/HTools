<!-- :: Batch section
@echo off
setlocal

echo Select an option:
for /F "delims=" %%a in ('mshta.exe "%~F0"') do set "HTAreply=%%a"
echo End of HTA window, reply: "%HTAreply%"
goto :EOF
-->


<HTML>
<HEAD>
<HTA:APPLICATION SCROLL="no" SYSMENU="no" >

<TITLE>HTA Buttons</TITLE>
<SCRIPT language="JavaScript">
window.resizeTo(374,100);

function closeHTA(reply){
   var fso = new ActiveXObject("Scripting.FileSystemObject");
   fso.GetStandardStream(1).WriteLine(reply);
   window.close();
}

</SCRIPT>
</HEAD>
<BODY>
   <button onclick="closeHTA(1);">First option</button>
   <button onclick="closeHTA(2);">Second option</button>
   <button onclick="closeHTA(3);">Third option</button>
</BODY>
</HTML>