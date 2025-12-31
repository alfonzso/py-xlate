FROM python:3.13-alpine

ENV FLASK_APP=/opt/py-xlate/app/main.py
WORKDIR /opt/py-xlate/

RUN apk --update add curl

ADD app/ app/
COPY pyproject.toml .
COPY poetry.lock .
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false && poetry install --no-root

ENTRYPOINT [ "flask", "run", "--host=0.0.0.0" ]
