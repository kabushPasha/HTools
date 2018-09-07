$window = new-object System.Windows.Window
$stackPanel = new-object System.Windows.Controls.StackPanel

$label = New-Object Windows.Forms.Label
$label.Location = New-Object Drawing.Point 50,30
$label.Size = New-Object Drawing.Point 250,30 
$label.text = "Enter your name and click the button"


$buttonNum = 20
for( $i = 0; $i -lt $buttonNum; $i++ )
{
    $button = new-object System.Windows.Controls.Button
    $button.Content = "Button Text" + $i
    $stackPanel.Children.Add( $button )
    $button.add_click({
    $i
    })
}





$scrollViewer = new-object System.Windows.Controls.ScrollViewer
$scrollViewer.Content = $stackPanel
$window.Content = $scrollViewer



$window.SizeToContent = [System.Windows.SizeToContent]::Width
$window.Height = 100
$window.ShowDialog()
