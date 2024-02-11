# Example File
import mlflow.pyfunc
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from lemma_tokenizer import LemmaTokenizer
from mlflow import MlflowClient

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

instrumentator = Instrumentator().instrument(app)


def fetch_latest_model():
    client = MlflowClient()
    return client.get_latest_versions()[0].name


def fetch_latest_version(model_name):
    model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/Production")
    return model


@app.on_event("startup")
async def startup():
    instrumentator.expose(app)

    LemmaTokenizer.download_assets()


@app.get("/predict/")
def model_output(text: str):
    print("Works I")
    model_name = "MultinomialNB"
    model = fetch_latest_version(model_name)

    print("Works II")
    input = np.array([text])

    prediction = model.predict(input)
    print(f"{prediction = }")
    return {"prediction": prediction[0].item()}
