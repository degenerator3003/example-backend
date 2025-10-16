#!/bin/sh

set -e

# generate self-signed certs for dev example if not present
if [ ! -f "$SSL_CERT_FILE" ] || [! -f "$SSL_KEY_FILE" ]; then
	echo "Generating self-signed TLS certs "
	mkdir -p /certs
	openssl req -x509 -newkey rsa:2048 -sha256 -days 3650 -nodes \
		-keyout "$SSL_KEY_FILE" -out "$SSL_CERT_FILE" \
		-subj "/CN=localhost" -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
fi


# wait for db port
python - <<'PY'
import os,time
import socket
host = 'db'; port=5432
for _ in range(60):
	s = socket.socket()
	s.settimeout(1)
	try:
		s.connect((host,port))
		s.close()
		break
	except Exeption:
		time.sleep(1)
PY

# seed if requested
if [ "$SEED_ON_START" = "true"  ]; then
	echo "Running DB migrations / create_all + seed"
	python -m app.seed
fi

# start server 
exec uvicorn app.main:app \
	--host ${UVICORN_HOST:-0.0.0.0} \
	--port ${UVICORN_PORT:-8443} \
	--ssl-keyfile "$SSL_KEY_FILE" \
	--ssl-certfile "$SSL_CERT_FILE"








