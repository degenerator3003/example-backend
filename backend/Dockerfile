
FROM python:3.12-alpine

# system deps for psycopg2, OpenSSL, etc.

RUN apk add --no-cache gcc musl-dev postgresql17-client postgresql17-dev openssl libffi-dev

# workdir

WORKDIR /app

# python deps
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# app code 
COPY ./app /app/app
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8443

ENV PUTHONUNBUFFERED=1

CMD ["/bin/sh","/app/entrypoint.sh"]




