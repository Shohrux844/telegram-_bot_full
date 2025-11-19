FROM python:3.10-alpine

WORKDIR /app

COPY . .

RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip install -r requirements.txt





