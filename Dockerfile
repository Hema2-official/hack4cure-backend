FROM python:3.12-bookworm

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install ghostscript python3-tk ffmpeg libsm6 libxext6 -y
RUN pip install -r requirements.txt --no-cache-dir

CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7000", "--reload" ]

EXPOSE 7000
