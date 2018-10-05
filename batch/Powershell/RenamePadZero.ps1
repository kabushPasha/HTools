$folder = "S:\\FPG\\s060\\Render\\004_FullRange"
$files = Get-ChildItem $folder

ForEach ($file in $files)
{
    $pieces = $file.BaseName.split(".",2)
    $base = $pieces[0].ToString().PadLeft(4,"0")
    #$base + "." + $pieces[1]
    if ($pieces.Count -gt 1)    {
        $base += "." + $pieces[1]
    }
    
    $in =  $folder  + "\" + $file.BaseName + $file.Extension
    $out = $folder  + "\" + $base  + $file.Extension
    
   Rename-Item $in $out
}