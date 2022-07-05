#!/bin/bash

curl -s -XPOST http://admin:admin@localhost:3000/api/auth/keys \
  -H "Content-Type: application/json" \
  -d '{"Name": "manually-added-user", "Role": "Admin"}' \
  | jq -r '.key' \
  | tee ~/.nosqlbench/grafana/grafana_apikey
