FROM continuumio/miniconda3

RUN mkdir /app
WORKDIR /app

COPY ../../requirements/requirements.app.txt .
RUN pip install -r requirements.app.txt

COPY /app .

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
