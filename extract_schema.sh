#! /usr/bin/bash
set -e

echo "Running Post-Sync Copy"
for podname in $(kubectl -n TEMPLATE get pods -l app=backend -o json| jq -r '.items[].metadata.name'); do
  kubectl cp TEMPLATE/"${podname}":/app/graphql/schema.graphql graphql/schema.graphql;
done
