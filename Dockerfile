FROM python:3.12-slim

# ставим компилятор и библиотеки для TA-Lib
RUN apt-get update && apt-get install -y \
    gcc g++ make \
    libta-lib0 libta-lib-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY main.py .
CMD ["python","main.py"]
