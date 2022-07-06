# https://cloud.google.com/ai-platform/training/docs/using-containers
# If your training configuration uses NVIDIA A100 GPUs, then your container must use CUDA 11 or later

FROM python:3.7-slim

ARG APP_HOME="/Repositories"
ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -y \
    curl \
    ffmpeg \
    rsync \
    software-properties-common \
    ssh \
    unzip \
    vim \
    python3-pip \
    wget && \
    apt-get clean

COPY requirements.txt /tmp/
WORKDIR /tmp/
RUN pip install -r requirements.txt
RUN pip install peekingduck==1.2.1 --no-dependencies

# COPY <repo_dir> <target location within Docker container>
COPY . ${APP_HOME}/PeekingDuck
WORKDIR ${APP_HOME}/PeekingDuck

EXPOSE 5000

CMD gunicorn main:app -w 1 -b :5000 -k uvicorn.workers.UvicornWorker