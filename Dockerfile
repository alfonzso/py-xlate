FROM python:3.9-alpine3.12

ENV FLASK_APP=/opt/py-xlate/app/app.py
WORKDIR /opt/py-xlate/

ADD app/ app/
ADD pip_freeze .
ADD run.sh .
RUN pip install -r pip_freeze

ENTRYPOINT [ "flask", "run", "--host=0.0.0.0" ]