FROM continuumio/miniconda3

WORKDIR /mlruns

COPY ../requirements/requirements.mlflow.txt .

RUN pip install -r requirements.mlflow.txt

EXPOSE 5000

CMD ["sh", "-c", "mlflow server --backend-store-uri sqlite:////mlruns/mlflow.db --default-artifact-root file:///mlruns --serve-artifacts --host=0.0.0.0"]
