import asyncio
import time


async def calc(n: int) -> int:
    print(n)
    await asyncio.sleep(1)
    print(n ** 2)
    return n ** 3


async def main():
    bum = [calc(x) for x in range(10)]
    return await asyncio.gather(*bum)

if __name__ == '__main__':
    s = time.perf_counter()
    res = asyncio.run(main())
    print(f'{res} in {time.perf_counter() - s} sec')
