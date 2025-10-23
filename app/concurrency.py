import os, asyncio
from contextlib import asynccontextmanager
from anyio import fail_after

SEM = asyncio.Semaphore(int(os.getenv('MAX_CONCURRENCY', '8')))

@asynccontextmanager
async def slot():
    async with SEM:
        yield

def with_timeout(seconds: float):
    return fail_after(seconds)
