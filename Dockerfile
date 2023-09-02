FROM continuumio/miniconda3:latest

RUN apt-get update && apt-get install -y binutils

WORKDIR /app
COPY . /app

RUN conda env create -n myenv -f /app/environment.yml

RUN conda run -n myenv pyinstaller --onefile /app/main.py

ENTRYPOINT ["/app/dist/main"]