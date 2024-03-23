from enum import Enum

import librosa
import mlflow.keras
import mlflow.tensorflow
import numpy as np
from fastapi import FastAPI, File, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from mlflow import MlflowClient

app = FastAPI()


class Country(str, Enum):
    LSTM = "LSTM"


# Allowing all origins, methods, and headers for CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def fetch_latest_model(name="LSTM"):
    """Fetches the latest model versions from MLflow."""
    client = MlflowClient()
    model_version = client.get_latest_versions(name)

    if model_version:
        return model_version[0].source
    else:
        return None


def extract_features(file):
    """Extracts MFCC features from the audio file."""
    audio, sample_rate = librosa.load(file)
    mfcc_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfcc_scaled_features = np.mean(mfcc_features.T, axis=0)
    return mfcc_scaled_features


def fetch_latest_version(model_name):
    """Loads the latest version of the specified model."""
    model = mlflow.tensorflow.load_model(f"models:/{model_name}/model")
    return model


@app.get("/predict/")
def predict_text(text: str):
    """Endpoint to predict output using a specified model."""
    model_name = "MultinomialNB"
    model = fetch_latest_version(model_name)
    input_data = np.array([text])
    prediction = model.predict(input_data)
    print(f"Prediction: {prediction}")
    return {"prediction": prediction[0].item()}


@app.get("/models")
def get_models(model: str = Query("LSTM", enum=["LSTM", "OTHER"])):  # noqa: B008
    """Endpoint to get the latest models."""
    models = fetch_latest_model(model)
    return {"models": models}


@app.post("/uploadfile/")
def upload_file(
    file: UploadFile = File(...),  # noqa: B008
    model_name: str = Query("LSTM", choices=("LSTM", "NO MODEL")),  # noqa: B008
):
    """Endpoint to upload an audio file and get prediction using a specified model."""
    return {"filename": file.filename, "prediction": "Toxic Audio", "model": model_name}
