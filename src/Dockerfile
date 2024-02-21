FROM prefecthq/prefect:2.11.5-python3.11

RUN mkdir /src
WORKDIR /src

COPY ../requirements/requirements.src.txt .

RUN pip install -r requirements.src.txt

COPY /src .

ENV PYTHONPATH /src
