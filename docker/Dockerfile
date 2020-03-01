FROM python:3.7-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry==1.* \
    && pip install "gunicorn <=20"

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

RUN poetry install --no-dev --no-interaction --no-ansi

COPY ./create_slack_bday_chat  /code/create_slack_bday_chat/
COPY docker/flask_cfg.py /data/
COPY docker/gunicorn_cfg.py /data/

ENV CREATE_SLACK_BDAY_CHAT_FLASK_CONFIG  /data/flask_cfg.py
ENV LOGURU_AUTOINIT 0

ENTRYPOINT ["gunicorn", "-c", "/data/gunicorn_cfg.py", "create_slack_bday_chat:app"]
