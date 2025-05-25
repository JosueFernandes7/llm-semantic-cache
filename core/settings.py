import os
from dotenv import load_dotenv
from langchain_redis import RedisConfig

load_dotenv()

# Ollama configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST") or "http://localhost:11434"

# Redis configuration
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or "mypassword"
REDIS_URL = os.getenv("REDIS_URL") or f"redis://:{REDIS_PASSWORD}@localhost:6379"
INDEX_NAME = os.getenv("INDEX_NAME") or "faq_index"

redis_config = RedisConfig(index_name=INDEX_NAME, redis_url=REDIS_URL)
