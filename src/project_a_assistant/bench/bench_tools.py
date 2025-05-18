
import asyncio, time, random
async def _dummy(name): await asyncio.sleep(random.uniform(0.01,0.02)); return name
async def bench(n=100):
    t0=time.time()
    await asyncio.gather(*[_dummy('x') for _ in range(n)])
    print(f"{n} calls in {time.time()-t0:.2f}s")
if __name__=='__main__':
    asyncio.run(bench())
