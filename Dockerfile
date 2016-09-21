FROM ubuntu:xenial
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN locale-gen en_CA.UTF-8
RUN apt-get update && apt-get install -y python3-pip git

RUN pip3 install django
RUN pip3 install virtualenv

RUN git clone https://github.com/andricDu/s2-scheduler.git
WORKDIR s2-scheduler

RUN virtualenv venv
RUN source venv/bin/activate

RUN pip3 install django gunicorn

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

CMD gunicorn SampleScheduler.wsgi --bind 0.0.0.0:8000

