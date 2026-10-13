$dllPath = "C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp\YACpkTool\CpkMaker.dll"
$asm = [System.Reflection.Assembly]::LoadFrom($dllPath)

$testDir = "C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp\test_dir_upd"
$testCpk = "C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp\test_upd.cpk"
$testOut = "C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp\test_upd_out.cpk"

New-Item -ItemType Directory -Path $testDir -Force | Out-Null
[System.IO.File]::WriteAllText("$testDir\a.txt", "original a")
[System.IO.File]::WriteAllText("$testDir\b.txt", "original b")

# 1. Build initial CPK
$m1 = New-Object CriCpkMaker.CpkMaker
$m1.CpkFileMode = [CriCpkMaker.CpkMaker+EnumCpkFileMode]::ModeFilename
$m1.AddFile("$testDir\a.txt", "a.txt", 0, $false) | Out-Null
$m1.AddFile("$testDir\b.txt", "b.txt", 0, $false) | Out-Null
$m1.StartToBuild($testCpk)
$m1.WaitForComplete() | Out-Null
$m1.Dispose()

# 2. Update b.txt in CPK using AnalyzeCpkFile
$replB = "$testDir\new_b.txt"
[System.IO.File]::WriteAllText($replB, "NEW UPDATED B CONTENT!")

$m2 = New-Object CriCpkMaker.CpkMaker
$m2.CpkFileMode = [CriCpkMaker.CpkMaker+EnumCpkFileMode]::ModeFilename
$m2.AnalyzeCpkFile($testCpk) | Out-Null
$m2.AddFile($replB, "b.txt", 0, $false) | Out-Null
$m2.StartToBuild($testOut)
$res = $m2.WaitForComplete()
$m2.Dispose()

Write-Host "Update result: $res"

# 3. Verify updated CPK
$m3 = New-Object CriCpkMaker.CpkMaker
$m3.AnalyzeCpkFile($testOut) | Out-Null
Write-Host "Files in testOut: $($m3.FileData.Count)"
$m3.Dispose()

# Cleanup
Remove-Item -Path $testDir -Recurse -Force
Remove-Item -Path $testCpk -Force
Remove-Item -Path $testOut -Force
