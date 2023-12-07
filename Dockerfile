FROM python:3.11.5-alpine3.17

WORKDIR /app

RUN apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev \
    && pip install --upgrade pip

COPY ./src ./

RUN pip install -r requirements.txt

RUN mkdir -p static/ && chmod -R 755 static/

CMD [ "sh", "-c", "python manage.py migrate && \
                python manage.py collectstatic --noinput --clear && \
                gunicorn backend.wsgi" ]