FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y gcc ffmpeg libsm6 libxext6
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

CMD ["python3", "-u", "main.py"]
