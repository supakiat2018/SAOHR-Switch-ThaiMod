$dllPath = "C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp\YACpkTool\CpkMaker.dll"
$asm = [System.Reflection.Assembly]::LoadFrom($dllPath)
$types = $asm.GetExportedTypes()
foreach ($t in $types) {
    Write-Host $t.FullName
}
