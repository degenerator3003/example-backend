#!/bin/bash

LOCALH='https://localhost:8443'


#---Health
echo 'health'
curl -k ${LOCALH}/

echo 'lists'
#---Lists
echo 'organizations'
curl -k ${LOCALH}/api/parties/organizations
echo " "

echo 'customers'
curl -k ${LOCALH}/api/parties/customers
echo " "

echo 'currencies'
curl -k ${LOCALH}/api/parties/currencies
echo " "

echo 'goods'
curl -k ${LOCALH}/api/goods/
echo " "

echo 'inventory'
curl -k ${LOCALH}/api/goods/inventory
echo " "

echo 'documents'
curl -k ${LOCALH}/api/documents/
echo " "


# Activate and deactivate SELL doc N:S-1001
echo 'Deactivate sell'
curl -k -X POST ${LOCALH}/api/documents/1/activate \
	-H 'Content-Type: application/json' -d '{"active":false}'
echo " "

echo 'Activate sell'
curl -k -X POST ${LOCALH}/api/documents/1/activate \
	-H 'Content-Type: application/json' -d '{"active":true}'
echo " "

echo 'inventory'
curl -k ${LOCALH}/api/goods/inventory
echo " "









