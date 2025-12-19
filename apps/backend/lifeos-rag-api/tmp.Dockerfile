FROM lifeos-rag-api-backend-api:latest
COPY src /app/src/
CMD ["python", "/app/src/insert_test_event.py"]