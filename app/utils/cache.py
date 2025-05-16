import redis, json, os
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379)

def get_cache(key):
    val = r.get(key)
    return json.loads(val) if val else None

def set_cache(key, data):
    r.set(key, json.dumps(data), ex=3600)  # 1-hour cache
