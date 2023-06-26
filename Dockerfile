FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN apt update; \
    apt-get install -y ffmpeg; \ 
    rm -rf /var/lib/apt/lists/*

CMD ["uvicorn", "MPextract:app"]