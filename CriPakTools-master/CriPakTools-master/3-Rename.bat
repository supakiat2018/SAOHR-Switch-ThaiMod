@echo off
setlocal enabledelayedexpansion
for /f %%a in ('dir /b/a-d/s *.out.xfbin') do (
  set "str=%%a"
  copy "%%a" "!str:.out=!"
  del "%%a"
)