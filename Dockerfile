FROM python:3.12-slim

# ставим только компилятор и wget
RUN apt-get update && apt-get install -y \
    gcc g++ make wget \
    && rm -rf /var/lib/apt/lists/*

# качаем и устанавливаем TA-Lib C-библиотеку вручную
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && make install && \
    cd .. && rm -rf ta-lib*

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY main.py .
CMD ["python","main.py"]
