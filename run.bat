@echo off

set env_folder=env
echo -------------------------------------------------------------------------------
echo Default Python Virtual Environment is ^/%env_folder%

:ask1
echo -------------------------------------------------------------------------------
echo Press [1] for Development Mode
echo Press [2] for Production Mode

set choice1Timeout=10
set defaultChoice1=2
choice /t %choice1Timeout% /c 12 /N /d %defaultChoice1% /m "(Decision will be %defaultChoice1% after %choice1Timeout% seconds) Your Choice ?"
rem The construct if errorlevel n checks if the errorlevel is at least n, therefor the way to do the test is go from higher errorlevel to lower errorlevel
if errorlevel 2 goto setToProduction
if errorlevel 1 goto setToDevelopment


:setToDevelopment
set FLASK_ENV=development
goto finishSetup

:setToProduction
set FLASK_ENV=production
goto finishSetup

:finishSetup
echo ^> flask environment variable will be set to %FLASK_ENV% later


:ask2
echo -------------------------------------------------------------------------------
echo Press [1] for Skipping project environment Setup
echo Press [2] for Preparing project environment Setup

set choice2Timeout=10
set defaultChoice2=1
choice /t %choice2Timeout% /c 12 /N /d %defaultChoice2% /m "(Decision will be %defaultChoice2% after %choice2Timeout% seconds) Your Choice ?"
rem The construct if errorlevel n checks if the errorlevel is at least n, therefor the way to do the test is go from higher errorlevel to lower errorlevel
if errorlevel 2 goto setupEnv
if errorlevel 1 goto skipSetupEnv


:setupEnv

if exist "%env_folder%\" (
    echo.
    echo -------------------------------------------------------------------------------
	echo ^ ^ ^> skipping creating python virtual environment
	echo -------------------------------------------------------------------------------
	echo [%env_folder%] Exists !
) else (

	rd /s /q "%env_folder%"
	echo.
	echo -------------------------------------------------------------------------------
	echo ^ ^ ^> creating python virtual environment [%env_folder%]
	echo -------------------------------------------------------------------------------
	python -m venv %env_folder%
)

echo.
echo -------------------------------------------------------------------------------
echo ^ ^ ^> activating python virtual environment ...
echo -------------------------------------------------------------------------------
call %env_folder%\Scripts\activate
echo virtual environment [%env_folder%] was activated

echo.
echo -------------------------------------------------------------------------------
echo ^ ^ ^> collecting python packages ...
echo -------------------------------------------------------------------------------
call pip install -r requirements.txt --upgrade

:skipSetupEnv

echo.
echo -------------------------------------------------------------------------------
echo ^ ^ ^> activating python virtual environment ...
echo -------------------------------------------------------------------------------
call %env_folder%\Scripts\activate
echo virtual environment [%env_folder%] was activated


echo.
echo -------------------------------------------------------------------------------
echo ^ ^ ^> setting flask environment variables ...
echo -------------------------------------------------------------------------------
call set FLASK_APP=app
echo FLASK_APP                      --^> app
call set FLASK_ENV=%FLASK_ENV%
echo FLASK_ENV                      --^> %FLASK_ENV%

echo.
echo -------------------------------------------------------------------------------
echo ^ ^ ^> run flask server ...
echo -------------------------------------------------------------------------------
call flask run -h 0.0.0.0 -p 5000