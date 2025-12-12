#!/bin/bash
# This script starts the backend services (FastAPI, etc.) in detached mode.
echo "Starting backend services..."
docker-compose -f apps/backend/lifeos-rag-api/docker-compose.yml up -d
