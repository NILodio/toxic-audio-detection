# TOXIC-AUDIO-DETECTION - Base Project 

## 🚨 Warning: Under Construction 😎 🏗️

This project is currently undergoing restructuring; please refrain from using it at the moment. Kindly wait for further updates.

In the next couple of months, it will be ready for use. 😎 🚀

---

## Develoment 😎 🏗️
--- 
### Prerequisites

Make sure you have `pyenv` installed on your local machine before proceeding.

## How to Use

To utilize this project, follow the steps below:

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

Install the dependencies

### Environment Variables

Create a `.env` file in the root directory of the project. Add the following environment variables to it: check `.env.example` for the required environment variables.

```bash
# .env
KAGGLE_USERNAME=
KAGGLE_KEY=
DATASET_RAW=fangfangz/audio-based-violence-detection-dataset

```

### Commands

To fetch the raw data, run the following command:

```bash
python src/scripts/fetch_raw_data.py
```
