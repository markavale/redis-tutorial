import redis

def redis_connection():
    PORT = 6379
    HOST = "localhost"
    client = redis.Redis(host=HOST, port=PORT, decode_responses=True, db=5)
    return client

