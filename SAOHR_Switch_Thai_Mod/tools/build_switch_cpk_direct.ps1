param(
    [string]$StagingDir = "C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp\SAOHR_Switch_Thai_Mod\build_staging\usa",
    [string]$OutCpk = "C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp\SAOHR_Switch_Thai_Mod\atmosphere\contents\0100EC400D54E000\romfs\pkg\usa.cpk"
)

$dllPath = "C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp\YACpkTool\CpkMaker.dll"
Write-Host "Loading CriCpkMaker library from $dllPath..."
$asm = [System.Reflection.Assembly]::LoadFrom($dllPath)
$cpk = New-Object CriCpkMaker.CpkMaker

$cpk.CpkFileMode = [CriCpkMaker.CpkMaker+EnumCpkFileMode]::ModeFilename
$cpk.DataAlign = 2048

$outDir = [System.IO.Path]::GetDirectoryName($OutCpk)
if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
}
if (Test-Path $OutCpk) {
    Remove-Item -Path $OutCpk -Force
}

Write-Host "Scanning files in $StagingDir..."
$files = Get-ChildItem -Path $StagingDir -Recurse -File
Write-Host "Found $($files.Count) files. Registering with CPK Maker..."

$cleanBase = $StagingDir.TrimEnd('\')
foreach ($f in $files) {
    $rel = $f.FullName.Substring($cleanBase.Length + 1).Replace('\', '/')
    $cpk.AddFile($f.FullName, $rel, 0, $false) | Out-Null
}

Write-Host "Starting build to: $OutCpk (Running native multi-threaded engine)..."
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$cpk.StartToBuild($OutCpk)
$success = $cpk.WaitForComplete()
$sw.Stop()

if ($success) {
    $size = (Get-Item $OutCpk).Length
    Write-Host "`nSUCCESS! Built usa.cpk in $($sw.Elapsed.TotalSeconds.ToString('F1')) seconds!"
    Write-Host "Path: $OutCpk"
    Write-Host "Size: $('{0:N0}' -f $size) bytes ($([Math]::Round($size / 1MB, 2)) MB)"
} else {
    Write-Host "`nFAILED to build CPK. Error: $($cpk.ErrorMessage)"
}

$cpk.Dispose()
