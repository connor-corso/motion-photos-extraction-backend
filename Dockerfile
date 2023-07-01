FROM python:3.9
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN apt update; \
    apt-get install -y ffmpeg; \ 
    rm -rf /var/lib/apt/lists/*

CMD ["uvicorn", "MPextract:app", "--host", "0.0.0.0", "--port", "80"]