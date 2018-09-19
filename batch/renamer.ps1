#foreach($child in Get-ChildItem)
#{
#	Write-Host $child.toString().replace("_4k","4k")
#}

 Get-ChildItem  -Recurse -Depth 2  * | Rename-Item -NewName { $_.name -Replace '_4k','' }