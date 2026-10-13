$dllPath = "C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp\YACpkTool\CpkMaker.dll"
$asm = [System.Reflection.Assembly]::LoadFrom($dllPath)
$cpk = New-Object CriCpkMaker.CpkMaker

$testDir = "C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp\test_fast_cpk"
$testOut = "C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp\test_fast.cpk"

New-Item -ItemType Directory -Path $testDir -Force | Out-Null
for ($i=0; $i -lt 50; $i++) {
    [System.IO.File]::WriteAllText("$testDir\f$i.txt", "content $i")
    $cpk.AddFile("$testDir\f$i.txt", "f$i.txt", 0, $false) | Out-Null
}

$sw = [System.Diagnostics.Stopwatch]::StartNew()
$cpk.StartToBuild($testOut)
$res = $cpk.WaitForComplete()
$sw.Stop()

Write-Host "WaitForComplete result: $res in $($sw.ElapsedMilliseconds) ms!"
$cpk.Dispose()
Remove-Item -Path $testDir -Recurse -Force
if (Test-Path $testOut) { Remove-Item -Path $testOut -Force }
