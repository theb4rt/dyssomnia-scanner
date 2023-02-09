FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=ms
ENV FLASK_DEBUG=1

RUN apk update \
    && apk add --no-cache \
        build-base \
        postgresql-dev	\
        python3-dev

WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .
RUN chmod a+rx ./start.sh

EXPOSE 5000
CMD ["./start.sh"]
