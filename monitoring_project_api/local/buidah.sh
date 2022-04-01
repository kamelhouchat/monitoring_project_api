ct=$(buildah from debian)
buildah run --user root $ct apt update -y
buildah run --user root $ct apt-get install python3.9 python3.pip python3-gunicorn -y
buildah run --user root $ct pip install --upgrade pip setuptools && useradd test
buildah config --user test $ct
buildah copy $ct ../../ /home/test/code
buildah run $ct pip install -r /home/test/code/requirements.txt
buildah run $ct \
echo -n "FLASK_SETTINGS_FILE=">/home/test/code/.env && \
python -c "import os; print(os.urandom(16))">>/home/test/code/.env && \
echo "">>/home/test/code/.env && \
echo "FLASK_ENV=production">>/home/test/code/.env && \
echo "FLASK_DEBUG=1">>/home/test/code/.env && \
echo -n "FLASK_SETTINGS_FILE=$(readlink -f /home/test/code/monitoring_project_api/config.py)">>/home/test/code/.env
buildah config --cmd  "gunicorn -w 4 -b 0.0.0.0:5000 /home/test/code/monitoring_project_api/__init__.py:create_app" $ct
