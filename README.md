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
