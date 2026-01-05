import time
from fastapi import HTTPException, status

LUA_INCR_EXPIRE = """
local current = redis.call("INCR", KEYS[1])
if current == 1 then
  redis.call("EXPIRE", KEYS[1], ARGV[1])
end
return current
"""

def enforce_rpm(redis_client, key_id: int, rpm_limit: int):
    window = int(time.time() // 60)  # current minute bucket
    rkey = f"rl:apikey:{key_id}:{window}"
    ttl_seconds = 70  # slightly > 60s

    count = redis_client.eval(LUA_INCR_EXPIRE, 1, rkey, ttl_seconds)

    if int(count) > int(rpm_limit):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded: {rpm_limit} rpm",
        )
