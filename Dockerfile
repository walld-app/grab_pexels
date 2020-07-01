FROM python:3.8.2-alpine3.11
# TODO make builder and executer
RUN apk update && apk add gcc postgresql-dev python3-dev musl-dev git --no-cache
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD python main.py