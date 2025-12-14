import os
from dotenv import load_dotenv

load_dotenv()

# --- Database Configuration ---
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "") # Keep empty for no authentication or provide a default
QDRANT_GRPC_PORT = int(os.getenv("QDRANT_GRPC_PORT", 6334)) # Default gRPC port for Qdrant

# --- Redis Configuration ---
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# --- ArangoDB Configuration ---
ARANGODB_HOST = os.getenv("ARANGODB_HOST", "http://localhost:8529")
ARANGODB_DB = os.getenv("ARANGODB_DB", "_system")
ARANGODB_USER = os.getenv("ARANGODB_USER", "root")
ARANGODB_PASSWORD = os.getenv("ARANGODB_PASSWORD", "root_password") # Change this!

# --- API Configuration ---
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# --- CORS Configuration ---
# Comma-separated list of allowed origins
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

# --- Logging ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# --- JWT Configuration ---
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key") # Change this in production!
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
