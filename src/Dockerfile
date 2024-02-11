FROM continuumio/miniconda3

RUN mkdir /src
WORKDIR /src

COPY ../requirements/requirements.src.txt .

RUN pip install -r requirements.src.txt

COPY /src .

# RUN prefect config set PREFECT_API_DATABASE_MIGRATE_ON_START="True"
RUN prefect config set PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://postgres:password@prefect-db:5432/prefect"
RUN prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
ENV MLFLOW_TRACKING_URI=http://mlflow:5000
CMD ["sh","-c","prefect server start --host 0.0.0.0 & sleep 5 && prefect deployment apply train-deployment.yaml & sleep 5 && prefect agent start -q 'default'"]
