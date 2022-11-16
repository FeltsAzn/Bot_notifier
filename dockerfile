FROM python:3.10.6-slim
WORKDIR /bot
COPY requirements.txt requirements.txt
COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]