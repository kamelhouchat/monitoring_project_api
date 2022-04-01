ct=$(buildah from debian)
buildah run --user root $ct apt update -y
buildah run --user root $ct apt-get install python3.9 python3.pip python3-gunicorn -y
buildah run $ct pip install --upgrade pip setuptools
buildah copy $ct ../../ ~/code
buildah run $ct pip install -r requirements.txt
buildah run $ct \
echo -n "FLASK_SETTINGS_FILE=">~/code/.env && \
python -c "import os; print(os.urandom(16))">>~/code/.env && \
echo "">>~/code/.env && \
echo "FLASK_ENV=production">>~/code/.env && \
echo "FLASK_DEBUG=1">>~/code/.env && \
echo -n "FLASK_SETTINGS_FILE=$(readlink -f ~/code/monitoring_project_api/config.py)">>~/code/.env
buildah config $ct --cmd  "gunicorn -w 4 -b 0.0.0.0:5000 ~/code/monitoring_project_api/__init__.py:create_app"
