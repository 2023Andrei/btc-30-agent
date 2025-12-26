FROM python:3.11-slim

# ставим только wget
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# качаем **актуальный** wheel для Python 3.11 x86_64
RUN wget https://files.pythonhosted.org/packages/cp311/t/ta_lib/TA_Lib-0.4.27-cp311-cp311-manylinux_2_28_x86_64.whl -O ta_lib.whl

COPY requirements.txt .
RUN pip install --upgrade pip && pip install ta_lib.whl && pip install -r requirements.txt

COPY main.py .
CMD ["python","main.py"]
