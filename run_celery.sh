source /home/nikhil/AviatorRepo/aviator_env/bin/activate
export PYTHONPATH=$PYTHONPATH:'/home/nikhil/AviatorRepo/dyfo'
celery worker -B --app=piWS -l info

