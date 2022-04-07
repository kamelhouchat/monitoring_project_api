FROM python:3.8.6
WORKDIR /monitoring_project_api
COPY requirements.txt requirements.txt
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
RUN flask setup-db
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
