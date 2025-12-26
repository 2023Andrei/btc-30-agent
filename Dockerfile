FROM python:3.11-slim

# ставим компилятор и заголовки
RUN apt-get update && apt-get install -y \
    gcc g++ make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY main.py .
CMD ["python","main.py"]
