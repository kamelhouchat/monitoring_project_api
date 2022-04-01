FROM debian
USER root 
RUN apt update -y
RUN apt-get install python3.9 python3.pip python3-gunicorn -y
RUN pip install --upgrade pip setuptools && useradd test
USER test
COPY ../../ /home/test/code
RUN pip install -r /home/test/code/requirements.txt
RUN \
echo -n "FLASK_SETTINGS_FILE=">/home/test/code/.env && \
python -c "import os; print(os.urandom(16))">>/home/test/code/.env && \
echo "">>/home/test/code/.env && \
echo "FLASK_ENV=production">>/home/test/code/.env && \
echo "FLASK_DEBUG=1">>/home/test/code/.env && \
echo -n "FLASK_SETTINGS_FILE=/home/test/code/monitoring_project_api/config.py">>/home/test/code/.env
CMD  ["gunicorn ", "-w", "4" ,"-b" ,"0.0.0.0:5000" ,"/home/test/code/monitoring_project_api/__init__.py:create_app"]