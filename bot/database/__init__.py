import redis as r
from getenv import env


MAX_CONNECTIONS = 15

redis = r.Redis.from_url(
    url=env('REDIS_DB_URL'),
    db=0,
    max_connections=MAX_CONNECTIONS
)
