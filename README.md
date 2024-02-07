# TOXIC-AUDIO-DETECTION - Project Under Construction 🏗️

## 🚨 Warning: This project is currently undergoing restructuring. 😎 

Please avoid using it at the moment and patiently await further updates.

Anticipated completion in the next couple of months. 😎 🚀

---

## Development 😎 🏗️
### Prerequisites

Ensure that `pyenv` is installed on your local machine before proceeding.

## How to Use

To make use of this project, follow the steps below:

### Create a Virtual Environment with Pipenv

```bash
pyenv virtualenv 3.10 toxic-audio
```

Activate the virtual environment before working on the project.

```bash
pyenv local toxic-audio
```

Install the dependencies

```bash
make develop
```

### Environment Variables

Create a `.env` file in the root directory of the project. Add the necessary environment variables; refer to `.env.example` for the required variables.

```bash
# .env
KAGGLE_USERNAME=
KAGGLE_KEY=
DATASET_RAW=fangfangz/audio-based-violence-detection-dataset
```

### Commands

To fetch the raw data, execute the following command:

```bash
python src/scripts/fetch_raw_data.py
```

---

## 🚀 Windows Instructions 🚀

### Install pyenv for Windows 😎
Run a PowerShell terminal as an administrator
Run the following command:
```bash
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```
If you are getting any UnauthorizedAccess error
Run the following command:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```
Now re-run the above installation command.
Installation complete!

After installation make sure that the pyenv variables are set in your machine environment variables.
`Windows > Edit the system environment variables > Environment Variables`
and check for the variables PYENV, PYENV_HOME, PYENV_ROOT.

The next step is to uninstall your current version of Python in Windows.

Now let's disable aliases related to Python
`Windows > Manage application execution aliases`
And disable all aliases related to Python

Pyenv for Windows is ready to be used! Please refer to this resource for the Windows pyenv commands.

https://pypi.org/project/pyenv-win/#validate

Let's install the python version for this project
Open a CMD in the project toxic-audio-detection
Run the following command:
```bash
pyenv install 3.10.0
```
Change the current python version using
```bash
pyenv global 3.10.0
pyenv local 3.10.0
```
Test your changes checking the python version on your shell. Output should be 3.10.0
```bash
pyenv shell 3.10.0
python -V
```

## How to set up `make` command on Windows 😎

Download mingw-get for Windows
https://sourceforge.net/projects/mingw/files/Installer/mingw-get-setup.exe/download

Run the installer and make sure the installation path has no whitespaces (Example: `C:\MinGW`)
Close the installer
Set mingw in your machine environment variables. Open:
`Windows > Edit the system environment variables > Environment Variables`
Edit the Path user variable and add the following path
`C:\MinGW\bin`
Save and close.

Open a terminal and run the following command
```bash
mingw-get install mingw32-make
```
Installation complete!
For more help, watch the following step by step video.
https://www.youtube.com/watch?v=taCJhnBXG_w

## (alternative-choco) How to set up `make` command on Windows 😎
1. open your powershell with admin privileges
2. run the following command
```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
``` 
3. close the powershell and open it again (allowing it to update)
4. run `choco install make`
5. it will automatically set the PATH in environment variables
6. go to the project repository and run `make build_notebook` and then `make start_notebook`

Currently --> it allows me to workon jupyter server, but the notebook is not inline with the common repo (updated_06_feb_24_evening)

## Cloning the project for Windows 😎
When working on Windows you have to clone the repository using the following command (to avoid Unix chars and makefile issues)

```bash
git clone https://github.com/NILodio/toxic-audio-detection.git --config core.autocrlf=input
```

## Install Docker Desktop for Windows 😎
https://www.docker.com/products/docker-desktop/

## Building the docker container and setting up the project 😎
Now that we have pyenv, make, and the project correctly cloned for Windows we can proceed to install dependencies and build our Docker container.

Open Docker Desktop and minimize it
Run the following commands in the project folder

```bash
pyenv install 3.10.0
pyenv global 3.10.0
pyenv local 3.10.0
mingw32-make install
mingw32-make develop
mingw32-make build_notebook
mingw32-make start_notebook
```

Open the container port: `http://localhost:8888/`
When asked for a token insert: `123`

Now you have access to the jupyter notebooks!

## Setting up the data fetcher from Kaggle 😎
Go to Kaggle.com and open your settings
On the API section Create New Token. A json file name `kaggle.json` should start downloading.
Create a new `.env` file in the project repository, copying it from the `example.env` file.
Replace your user and token from the `kaggle.json` file into the new `.env` file.

Add or replace the kaggle.json file into the following path of your machine.
`C://Users//<Your username>//.kaggle//kaggle.json`

Open a terminal in the project folder and run the following command:
```bash
python src/scripts/fetch_raw_data.py
```
The data should start downloading under `/data` within the project repository.

Important: you should be on the project's Python version using pyenv, and with the version set globally and locally. Check previous pyenv steps.
