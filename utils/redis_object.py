import aioredis
from utils.const import TESTING, TEST_REDIS_URL, IS_LOAD_TEST

redis = None


async def check_test_redis():
    global redis
    if TESTING or IS_LOAD_TEST:
        redis = await aioredis.create_redis_pool(TEST_REDIS_URL)
