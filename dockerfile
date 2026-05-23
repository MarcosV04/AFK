FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python", "main.py"]