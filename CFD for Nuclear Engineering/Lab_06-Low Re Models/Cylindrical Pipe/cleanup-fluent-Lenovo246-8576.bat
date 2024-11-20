echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="D:\Ansys\ANSYS Inc\ANSYS Student\v242\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "D:\Ansys\ANSYS Inc\ANSYS Student\v242\fluent\ntbin\win64\tell.exe" Lenovo246 52386 CLEANUP_EXITING
timeout /t 1
"D:\Ansys\ANSYS Inc\ANSYS Student\v242\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="Lenovo246" (%KILL_CMD% 17368) 
if /i "%LOCALHOST%"=="Lenovo246" (%KILL_CMD% 16808) 
if /i "%LOCALHOST%"=="Lenovo246" (%KILL_CMD% 2388) 
if /i "%LOCALHOST%"=="Lenovo246" (%KILL_CMD% 6088) 
if /i "%LOCALHOST%"=="Lenovo246" (%KILL_CMD% 8576) 
if /i "%LOCALHOST%"=="Lenovo246" (%KILL_CMD% 5504)
del "C:\Users\Simone Pagliuca\Documents\GitHub\Fission-Reactor-Physics\CFD for Nuclear Engineering\Lab_06-Low Re Models\Cylindrical Pipe\cleanup-fluent-Lenovo246-8576.bat"
