FROM python:3.12

WORKDIR /swebapp
COPY . .
RUN ["pip", "install", "-r", "requirements.txt"]

CMD ["python", "Sport_server.py"]