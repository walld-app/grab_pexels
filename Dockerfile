FROM python:3.8.2-alpine3.11
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD python main.py