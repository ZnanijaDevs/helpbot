import os
import redis as r


redis = r.Redis(
    host=os.environ['REDIS_HOST'],
    port=os.environ['REDIS_PORT'],
    password=os.environ['REDIS_PASS'],
    username=os.environ['REDIS_USERNAME'],
    db=0,
)
