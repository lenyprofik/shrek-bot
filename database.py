
import os
import asyncpg
import logging

logger = logging.getLogger("shrek-db")
DATABASE_URL = os.getenv("DATABASE_URL")
_pool = None

async def init_db():
    global _pool
    if not DATABASE_URL:
        logger.error("DATABASE_URL není nastaven.")
        return
    _pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=5)
    async with _pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            xp INTEGER NOT NULL DEFAULT 0,
            level INTEGER NOT NULL DEFAULT 1,
            title TEXT DEFAULT '',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            last_seen TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
        """)
    logger.info("Databáze inicializována a pool vytvořen.")

async def get_user(user_id: int):
    async with _pool.acquire() as conn:
        row = await conn.fetchrow("SELECT user_id, xp, level, title FROM users WHERE user_id=$1", user_id)
        if not row:
            await conn.execute("INSERT INTO users(user_id) VALUES($1) ON CONFLICT DO NOTHING", user_id)
            row = await conn.fetchrow("SELECT user_id, xp, level, title FROM users WHERE user_id=$1", user_id)
        return dict(row)

async def add_xp(user_id: int, amount: int):
    async with _pool.acquire() as conn:
        await conn.execute("INSERT INTO users(user_id) VALUES($1) ON CONFLICT DO NOTHING", user_id)
        await conn.execute("UPDATE users SET xp = xp + $1, last_seen = now() WHERE user_id = $2", amount, user_id)

async def set_level_and_title(user_id: int, level: int, title: str):
    async with _pool.acquire() as conn:
        await conn.execute("INSERT INTO users(user_id) VALUES($1) ON CONFLICT DO NOTHING", user_id)
        await conn.execute("UPDATE users SET level=$1, title=$2 WHERE user_id=$3", level, title, user_id)