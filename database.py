import os
import asyncpg

db = None

async def init_db():
    global db
    db = await asyncpg.create_pool(
        dsn=os.getenv("DATABASE_URL"),
        min_size=1,
        max_size=5
    )

    async with db.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                xp INTEGER NOT NULL DEFAULT 0,
                level INTEGER NOT NULL DEFAULT 1,
                title TEXT DEFAULT 'Cibulový učedník',
                messages_in_level_channel INTEGER NOT NULL DEFAULT 0,
                commands_used INTEGER NOT NULL DEFAULT 0,
                nice_answers_received INTEGER NOT NULL DEFAULT 0,
                last_event_timestamp BIGINT DEFAULT 0
            );
        """)

    print("✅ Databáze připojena a tabulka users připravena.")


async def get_user(user_id: int):
    async with db.acquire() as conn:
        user = await conn.fetchrow(
            "SELECT * FROM users WHERE user_id = $1",
            user_id
        )
        if user is None:
            await conn.execute(
                "INSERT INTO users (user_id) VALUES ($1)",
                user_id
            )
            user = await conn.fetchrow(
                "SELECT * FROM users WHERE user_id = $1",
                user_id
            )
        return user


async def add_xp(user_id: int, amount: int):
    async with db.acquire() as conn:
        await conn.execute(
            "UPDATE users SET xp = xp + $1 WHERE user_id = $2",
            amount, user_id
        )


async def set_level_and_title(user_id: int, level: int, title: str):
    async with db.acquire() as conn:
        await conn.execute(
            "UPDATE users SET level = $1, title = $2 WHERE user_id = $3",
            level, title, user_id
        )