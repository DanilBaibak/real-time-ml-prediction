FROM python:3.8.6-slim

LABEL maintainer="danil.baibak@gmail.com"

RUN apt-get update \
    && apt-get install -y apt-utils sudo gcc postgresql-client libpq-dev \
    && apt autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV PYTHONPATH="${PYTHONPATH}:/ml_app"
WORKDIR "/ml_app"

COPY docker/requirements.txt .
COPY ../src .

RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --progress-bar off -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 80
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
