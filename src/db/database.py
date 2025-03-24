import asyncpg


class Database:
    def __init__(self, config):
        self.config = config
        self.pool = None

    async def connect(self):
        if self.pool is None:
            self.pool = await asyncpg.create_pool(**self.config)

    async def close(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def fetch(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def execute(self, query, *args):
        async with self.pool.acquire() as conn:
            await conn.execute(query, *args)
