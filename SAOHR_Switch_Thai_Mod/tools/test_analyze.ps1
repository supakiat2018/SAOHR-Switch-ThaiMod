$dllPath = "C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp\YACpkTool\CpkMaker.dll"
$asm = [System.Reflection.Assembly]::LoadFrom($dllPath)
$cpk = New-Object CriCpkMaker.CpkMaker

$testCpk = "C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp\SAOHR_Switch_Thai_Mod\atmosphere\contents\0100EC400D54E000\romfs\pkg\usa.cpk"
$res = $cpk.AnalyzeCpkFile($testCpk)
Write-Host "AnalyzeCpkFile result: $res"
Write-Host "Total files registered: $($cpk.FileData.Count)"
$cpk.Dispose()
