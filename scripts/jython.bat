set WAS_HOME=%1
set REMOTE_HOST=%2
set SOAP_PORT=%3
set USERNAME=%4
set PASSWORD=%5
set MODE=%6
set APPLICATION_PATH=%7
set APPNAME=%8
set PARAMS=%9

%WAS_HOME%\bin\wsadmin.bat -lang jython -conntype SOAP ^
-host %REMOTE_HOST% -port %SOAP_PORT% ^
-username %USERNAME% -password %PASSWORD% ^
-f ..\scripts\deploy.py %MODE% %APPLICATION_PATH% %APPNAME% %PARAMS%