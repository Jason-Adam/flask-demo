FROM python:3.7

RUN apt-get update

COPY ./requirements.txt /tmp/requirements.txt
WORKDIR /tmp
RUN pip3 install -r requirements.txt

COPY . /api
WORKDIR /
RUN chmod -x api/run_app.sh

CMD ["/bin/sh", "api/run_app.sh"]
