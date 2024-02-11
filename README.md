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
### bug fix on notebook - docker container

1. use git bash as of now 
2. change the token as follows in line 8 `c.NotebookApp.token = ""  ` file location `toxic-audio-detection\conf\.jupyter\jupyter_notebook_config.py`
3. save it and build the docker image 
4. run the container from git bash

tadah!! it works right? 🥳
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
C:\Users\bhair\Desktop\canada_study_permit\Class_AIML\term_2\AML_2404_Lab\git_repo\toxic-audio-detection\conf\.jupyter\jupyter_notebook_config.py
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

# Overview 🏗️

The full setup consists of three steps:
1) Training - A training script trains a model for the Threat dataset with sklearn, training is orchestrated by prefect and the models metrics and artifacts (the actual models) are uploaded to mlflow. 

2) Serving - The model is pulled and FastAPI delivers the prediction, a streamlit app serves as the user interface.


The individual services are packaged as docker containers and setup with docker compose.

## How to use

**Prerequisite**: Install Docker

**Start docker compose (from project folder)**

```
    docker compose up --build
    or
    make up
```

**Access individual services**

- Prefect `http://localhost:4200`
- mlflow `http://localhost:5000`
- FastAPI (to test) `http://localhost:8086/docs`
- Streamlit UI `http://localhost:8501`

**Create example model**

Run deployment in Prefect UI, deploy model artifacts in mlflow, tag it with "production" in mflow.

**Note**: The UI will only work if there is one "production" model in mlflow.

## Services

### 1) Docker and docker compose

`docker-compose.yaml` contains the definitions for all services. 
For every service it contains the docker image (either through `build` if based on a Dockerfile, or through `image` if a remote image). 
Also it opens the relevant ports within your "docker compose network", so that the services can communicate with each other. 
Additionally, a common volume for all containers that use mlflow is created and mounted into `/mlruns`. For Prometheus/Grafana a few configuration files are also mounted.

To initialize all services the command `docker compose up` can be used from the project folder.

### 2+3) Training script and prefect

The training script and prefect (for orchestration) are packaged into one service. 

The **training script** is placed under `src/model_training.py`.

The `train` function is wrapped into an `mlflow` flow operator. Also, it uses mlflow autolog.

**prefetc** is an orchestration tool and can therefore be used to schedule, monitor and organize jobs.

Based on the training script, a **prefect deployment file** `train-deployment.yaml` is generated using the following command:

`prefect deployment build src/model_training.py:train` 

The **Dockerfile** ultimately glues these components together. It
1) Creates folders
2) Installs requirements.txt
3) Sets the `PREFECT_API_URL` and `MLFLOW_TRACKING_URI`*
4) Starts the server, pushes the deployment and starts an agent**

*Using docker you can refer to the containers ip using `host.docker.internal` and refer to the other services with their docker compose name, e.g `http://mlflow:5000`

**In this project the prefect server and the agent (who executes the scripts) are on one container.


### 4) FastAPI

**FastAPI** is a framework for high-performance API. In this project I implemented a `/predict` endpoint. If that endpoint is queried
it will download the latest model from mlflow and output the prediction. Additionally, **prometheus_fastapi_instrumentator** scrapes events and sends them to Prometheus.

**Please note**: Currently the script will fetch the first model that is in production. It won't show any error if there is 
no model or there are multiple models.

### 7) Streamlit

**Streamlit** is a Python library to rapidly build UIs. The app is very simple and only passes input to the API to retrieve results.

## Limitations

**Multiple host machines: Kubernetes**

This project is meant to be deployed on a single host machine. In practice, you might want to use Kubernetes to deploy it 
on multiple instances to gain more isolation and scalability. **Kompose** could be an option to convert your docker compose file
to Kubernetes yaml. 

**Storage on cloud**

All artifacts, logs, etc. are saved locally/on docker volumes. In practice, you would save them to the cloud.

**Advanced Security**

Security - of course. Authentication, SSL encryption, API authentication and what not.
Good example using nginx. [Example](https://towardsdatascience.com/deploy-mlflow-with-docker-compose-8059f16b6039
)

## References
