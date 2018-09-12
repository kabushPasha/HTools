#powershell.exe yourpsscript.ps1 -windowstyle hidden

param (

    [switch]$cs = $false
 )

 $scriptFilename = $MyInvocation.MyCommand.Name
 
 function CreateShortcut
 {
     # Create Shortcut
    $WshShell = New-Object -ComObject WScript.Shell
    # Target is this script minus 
    #$target = $MyInvocation.ScriptName
    $Shortcut = $WshShell.CreateShortcut("$Home\Desktop\"+$scriptFilename +".lnk")
    $Shortcut.TargetPath = "powershell"
    $Shortcut.Arguments = '-File "' + $PSScriptRoot + '\' + $scriptFilename + '" -WindowsStyle Hidden'
    # windows style minimised is 7
    $Shortcut.WindowStyle = 7
    $Shortcut.Save() 
 }

 function CreateForm
 {
    Add-Type -AssemblyName System.Windows.Forms
    $Form = New-Object system.Windows.Forms.Form
    $Form.Text = "Harbor v2.0"

    # Resize
    $Form.Width = 100
    $Form.Height = 200
    $Form.AutoSize = $True
    $Form.AutoSizeMode = "GrowOnly"

    # Additional form window settings
    $Form.MinimizeBox = $False
    $Form.MaximizeBox = $False
    $Form.WindowState = "Normal"             # Maximized, Minimized, Normal
    $Form.SizeGripStyle = "Hide"             # Auto, Hide, Show
    $Form.ShowInTaskbar = $False
    #$Form.Opacity = 0.7                     # 1.0 is fully opaque; 0.0 is invisible
    $Form.StartPosition = "CenterScreen"     # CenterScreen, Manual, WindowsDefaultLocation, WindowsDefaultBounds, CenterParent

    # Label
    $Label = New-Object System.Windows.Forms.Label
    $Label.Text = "Press buttons to run scripts"
    $Label.AutoSize = $True
    $Form.Controls.Add($Label)


    <#
    $buttonNum = 20
    for( $i = 0; $i -lt $buttonNum; $i++ )
    {
        $y = 90 + $i*25
        
        $button = New-Object Windows.Forms.Button
        $button.text = "Name" + $i
        $button.Location = New-Object Drawing.Point 100,$y
        $button.Size = New-Object Drawing.Point 210,25
        
        $button.add_click({
            $Label.Text = $i
        }.GetNewClosure())

        $form.controls.add($button)
    }
    #>

    # LOAD All Custom Scripts located in batch folder
    $scripts = ls $PSScriptRoot/batch
    $y = 0
     foreach ($script in $scripts) {
        $y += 30
        
        $button = New-Object Windows.Forms.Button
        $button.text = $script
        $button.Location = New-Object Drawing.Point 0,$y
        $button.Size = New-Object Drawing.Point 200,25
        
        $button.add_click({
            $Label.Text = $i
            start $PSScriptRoot/batch/$script
        }.GetNewClosure())

        $form.controls.add($button)
     }


     # Create shortcuts for all commands
     <#
    $commands = Get-Content -Path $PSScriptRoot/commands.txt
     foreach ($command in $commands) {
        $y += 30        
        $button = New-Object Windows.Forms.Button
        $button.text = $command
        $button.Location = New-Object Drawing.Point 0,$y
        $button.Size = New-Object Drawing.Point 210,25
        #$command    
        $button.add_click({
            start $command
        }.GetNewClosure())

        $form.controls.add($button)
     }
     #>

     $json = (Get-Content -Raw -Path $PSScriptRoot/commands.json) | ConvertFrom-Json

    $names = $json.PSObject.Properties.Name
    foreach ($name in $names)
    {
        #$json.$name
        $y += 30        
        $button = New-Object Windows.Forms.Button
        $button.text = $name
        $button.Location = New-Object Drawing.Point 0,$y
        $button.Size = New-Object Drawing.Point 200,25
        #$command    
        $button.add_click({
            Invoke-Expression $json.$name
        }.GetNewClosure())

        $form.controls.add($button)
    }

    # Fix Position
    $Form.StartPosition = "Manual";
    Add-Type -AssemblyName System.Windows.Forms
    $screens = [System.Windows.Forms.Screen]::AllScreens
    $width = $screens[0].WorkingArea.Width
    $height = $screens[0].WorkingArea.Height

    #$width -= $Form.Width
    $height -= $Form.Height
    $Form.Location =  New-Object Drawing.Point $width,$height

    $Form.ShowDialog()
 }





if($cs)
{
   CreateShortcut
}
else
{
    CreateForm
}