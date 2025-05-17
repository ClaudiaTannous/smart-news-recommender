from app.services.redis_client import redis_client as r
import json

def get_cache(key):
    val = r.get(key)
    return json.loads(val) if val else None

def set_cache(key, data, ttl=3600):
    r.set(key, json.dumps(data), ex=ttl)  # 1-hour default TTL
