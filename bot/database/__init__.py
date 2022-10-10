import redis as r
from getenv import env


redis = r.Redis(
    host=env('REDIS_HOST'),
    port=env('REDIS_PORT'),
    password=env('REDIS_PASS'),
    username=env('REDIS_USERNAME'),
    db=0,
    max_connections=15
)
