
FROM python:3.6-slim-buster as app
# RUN apk add --no-cache mariadb-dev build-base


RUN apt-get update\
 && apt-get install -y gcc libmariadb-dev

RUN apt-get install -y wkhtmltopdf

RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends \
        wget git-core locales less \
        binutils libproj-dev gdal-bin \
    && rm -rf /var/lib/apt/lists/* \
    && echo 'alias ll="ls -l"' >> ~/.bashrc \
    && echo 'alias la="ls -la"' >> ~/.bashrc \
    && locale-gen

COPY requirements.txt /app/requirements.txt

WORKDIR app

RUN pip install -r requirements.txt
COPY . /app

# RUN pip install mysqlclient
# COPY --from=builder /root/.local /root/.local
# COPY --from=builder /app/ /app/
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

ENV PATH=/root/.local/bin:$PATH
ENTRYPOINT gunicorn api.wsgi --workers=1 --threads=2 --worker-class=gthread --bind 0.0.0.0:8080 --log-level debug
