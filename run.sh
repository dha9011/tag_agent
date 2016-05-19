#/bin/bash

FILEPATH=$(cd "$(dirname "$0")"; pwd)
#
#if [ -f /usr/local/bin/gunicorn ]
#    then
#    gunicorn_bin=/usr/local/bin/gunicorn
#elif
#    [ -f /usr/bin/gunicorn ]
#    then
#    gunicorn_bin=/usr/bin/gunicorn
#elif
#    [ -f /opt/t_agent/bin/gunicorn ]
#    then
#    gunicorn_bin=/opt/t_agent/bin/gunicorn
#else
#    echo 'Can not find gunicorn binary'
#    exit 1
#fi

daemon=`echo $1`
if [ "$daemon" == "-D" ]
then
nohup gunicorn app:app -c $FILEPATH/gunicorn.conf.py 1>/tmp/app_mgmt.log 2>&1 &
else
gunicorn app:app -c $FILEPATH/gunicorn.conf.py
fi