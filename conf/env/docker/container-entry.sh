#!/usr/bin/env bash

source /app_bin/runner.sh

run_python_script "Coletando arquivos estáticos" "manage.py collectstatic --noinput"
run_python_script_with_output "Migrating" "manage.py migrate"

echo " > Iniciando SERVER"
echo ;
echo "########################################################################"
echo ;
source /app_conf/env/docker/uwsgi-env.sh
uwsgi --enable-threads --cache 5000 --thunder-lock --show-config --static-map /static/=/code/static/ --static-map /media/=/code/media/
