echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="D:\Ansys\ANSYS Inc\ANSYS Student\v242\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "D:\Ansys\ANSYS Inc\ANSYS Student\v242\fluent\ntbin\win64\tell.exe" Lenovo246 50279 CLEANUP_EXITING
timeout /t 1
"D:\Ansys\ANSYS Inc\ANSYS Student\v242\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="Lenovo246" (%KILL_CMD% 10844) 
if /i "%LOCALHOST%"=="Lenovo246" (%KILL_CMD% 7592) 
if /i "%LOCALHOST%"=="Lenovo246" (%KILL_CMD% 7224) 
if /i "%LOCALHOST%"=="Lenovo246" (%KILL_CMD% 7816) 
if /i "%LOCALHOST%"=="Lenovo246" (%KILL_CMD% 8752) 
if /i "%LOCALHOST%"=="Lenovo246" (%KILL_CMD% 9540)
del "C:\Users\Simone Pagliuca\Documents\GitHub\Fission-Reactor-Physics\CFD for Nuclear Engineering\Lab_06-Low Re Models\Square Pipe\cleanup-fluent-Lenovo246-8752.bat"
