$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$Home\Desktop\Calc.lnk")
$Shortcut.TargetPath = "powershell"
$Shortcut.Arguments = '-File "' + $PSScriptRoot + '\Harbor.ps1"' + " -WindowsStyle Hidden "
$Shortcut.Save()