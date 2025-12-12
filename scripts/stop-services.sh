#!/bin/bash
# This script stops the backend services.
echo "Stopping backend services..."
docker-compose -f apps/backend/lifeos-rag-api/docker-compose.yml down
