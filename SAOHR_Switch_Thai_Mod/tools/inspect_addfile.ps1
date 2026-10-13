$dllPath = "C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp\YACpkTool\CpkMaker.dll"
$asm = [System.Reflection.Assembly]::LoadFrom($dllPath)
$type = $asm.GetType("CriCpkMaker.CpkMaker")
$methods = $type.GetMethods() | Where-Object { $_.Name -eq "AddFile" }
foreach ($m in $methods) {
    Write-Host "AddFile overload:"
    foreach ($p in $m.GetParameters()) {
        Write-Host "  $($p.ParameterType.Name) $($p.Name)"
    }
}
