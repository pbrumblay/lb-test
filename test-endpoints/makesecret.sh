#!/usr/bin/env bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=echo-tls/O=echo-tls"
kubectl create secret generic echo-tls --from-file=tls.crt --from-file=tls.key
