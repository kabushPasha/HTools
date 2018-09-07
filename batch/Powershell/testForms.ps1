#https://blogs.technet.microsoft.com/stephap/2012/04/23/building-forms-with-powershell-part-1-the-form/

Add-Type -AssemblyName System.Windows.Forms
$Form = New-Object system.Windows.Forms.Form
$Form.Text = "Sample Form"

# Create Label
$Label = New-Object System.Windows.Forms.Label
$Label.Text = "This form is very simple."
$Label.AutoSize = $True
$Form.Controls.Add($Label)

# Autosize
$Form.AutoSize = $True
$Form.AutoSizeMode = "GrowOnly"

$Form.Width = 500
$Form.Height = 200

# Additional form window settings
$Form.MinimizeBox = $False
$Form.MaximizeBox = $False
$Form.WindowState = "Normal"             # Maximized, Minimized, Normal
$Form.SizeGripStyle = "Hide"             # Auto, Hide, Show
$Form.ShowInTaskbar = $False
#$Form.Opacity = 0.7                     # 1.0 is fully opaque; 0.0 is invisible
$Form.StartPosition = "CenterScreen"     # CenterScreen, Manual, WindowsDefaultLocation, WindowsDefaultBounds, CenterParent

#########################################################
# LABEL
# Create the label control and set text, size and location
$label = New-Object Windows.Forms.Label
$label.Location = New-Object Drawing.Point 50,30
$label.Size = New-Object Drawing.Point 250,30 
$label.text = "Enter your name and click the button"

# TEXTBOX
# Create TextBox and set text, size and location
$textfield = New-Object Windows.Forms.TextBox
$textfield.Location = New-Object Drawing.Point 50,60
$textfield.Size = New-Object Drawing.Point 210,15

# BUTTON 
# Create Button and set text and location
$button = New-Object Windows.Forms.Button
$button.text = "Name"
$button.Location = New-Object Drawing.Point 100,100

# INPUT HANDLER BUTTON – ON CLICK IN THIS CASE
# Set up event handler to exit
$button.add_click({
$label.Text = "Hello " + $textfield.text
})

# CANCEL BUTTON 
# Create Button and set text and location
$button2 = New-Object Windows.Forms.Button
$button2.text = "Cancel"
$button2.Location = New-Object Drawing.Point 100,130

# INPUT HANDLER CANCEL BUTTON – CLOSE APP
# close button – on click close app
$button2.add_click({
$form.Close()
})

# ADD CONTROLS TO FORM
$form.controls.add($button)
$form.controls.add($button2)
$form.controls.add($label)
$form.controls.add($textfield)

$Form.ShowDialog()




