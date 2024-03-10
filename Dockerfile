FROM python:3.10

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /app

CMD ["python3", "./server.py"]
