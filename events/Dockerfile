FROM python:latest

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8888

ENTRYPOINT [ "python" ]
CMD [ "events.py" ]


