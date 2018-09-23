$folder = "C:\SDrive\Mega\Projects\2018\027_Scans\Render\\007_HornsRender"
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