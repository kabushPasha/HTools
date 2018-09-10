$json = (Get-Content -Raw -Path $PSScriptRoot/commands.json) | ConvertFrom-Json

$names = $json.PSObject.Properties.Name
foreach ($name in $names)
{
    $json.$name
}