FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y ffmpeg

RUN mkdir /src
WORKDIR /src

# Copy the requirements file and install dependencies
COPY requirements/requirements.src.txt .
RUN pip install -r requirements.src.txt

# Copy the rest of your source code
COPY . .

# Set the Python path
ENV PYTHONPATH=/src
