# kingbinary
scp -r /media/divine/Divine/Personal/Projects/Python/kingbinary/* root@198.54.112.149:/root/server
# read live logs
tail -f -n10 ./logs/gunicorn.info.log
# stop gunicorn
pkill gunicorn
# start gunicorn
gunicorn -c gunicorn.ini.py main:app
