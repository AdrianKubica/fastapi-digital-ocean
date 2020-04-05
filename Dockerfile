FROM tiangolo/uvicorn-gunicorn-fastapi

#WORKDIR fastapi
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./