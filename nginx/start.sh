#!/bin/sh

set -e

## Setup public key pinning (HPKP)
## See: https://developer.mozilla.org/en-US/docs/Web/Security/Public_Key_Pinning
# Get the SPKI fingerprint
FINGERPRINT=`openssl x509 -in /certs/server.crt -pubkey -noout | openssl rsa -pubin -outform der | openssl dgst -sha256 -binary | base64`
# Add it to our nginx config
cat <<EOF > /etc/nginx/conf.d/dinheiro/hpkp.conf
add_header Public-Key-Pins 'pin-sha256="${FINGERPRINT}"; max-age=5184000; includeSubDomains';
EOF

nginx
