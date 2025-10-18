import asyncio
from functools import wraps

async def async_retry(tries=3, delay=1, backoff=2):
    def deco(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    print(f"Retrying in {mdelay} seconds... ({e})")
                    await asyncio.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return await func(*args, **kwargs)
        return wrapper
    return deco
