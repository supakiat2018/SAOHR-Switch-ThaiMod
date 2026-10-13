$dllPath = "C:\Users\Supakiat\Downloads\Sword Art Online Hollow Realization nsp\YACpkTool\CpkMaker.dll"
$asm = [System.Reflection.Assembly]::LoadFrom($dllPath)
$cpk = New-Object CriCpkMaker.CpkMaker
$cpk | Get-Member -MemberType Property | Select-Object Name, Definition
