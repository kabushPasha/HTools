#powershell.exe yourpsscript.ps1 -windowstyle hidden

Add-Type -AssemblyName System.Windows.Forms
$Form = New-Object system.Windows.Forms.Form
$Form.Text = "Sample Form"

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
    $button.Size = New-Object Drawing.Point 210,25
        
    $button.add_click({
        $Label.Text = $i
        start $PSScriptRoot/batch/$script
    }.GetNewClosure())

    $form.controls.add($button)
 }


 # Create shortcuts for all commands
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


$Form.ShowDialog()