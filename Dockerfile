FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

COPY /home/.aws /root/.aws

CMD ["python3", "-u", "main.py"]
