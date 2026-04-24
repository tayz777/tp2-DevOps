from contextlib import asynccontextmanager

import aiomysql
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import os

# ── Configuration ─────────────────────────────────────────────────────────────
MONGO_URL = os.getenv("MONGO_URL", "mongodb://admin:password@db_mongo:27017/blog_db?authSource=admin")

MYSQL_HOST = os.getenv("MYSQL_HOST", "db_mysql")
MYSQL_DB = os.getenv("MYSQL_DATABASE", "app_db")
MYSQL_USER = os.getenv("MYSQL_USER", "appuser")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")

# ── Connexion MongoDB ──────────────────────────────────────────────────────────
mongo_client = AsyncIOMotorClient(MONGO_URL)
db_mongo = mongo_client.blog_db

# ── Pool de connexions MySQL (créé au démarrage) ───────────────────────────────
mysql_pool = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global mysql_pool
    mysql_pool = await aiomysql.create_pool(
        host=MYSQL_HOST,
        db=MYSQL_DB,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        autocommit=True,
    )
    yield
    mysql_pool.close()
    await mysql_pool.wait_closed()


app = FastAPI(lifespan=lifespan)


# ── Route 1 : articles MongoDB ────────────────────────────────────────────────
@app.get("/posts")
async def get_posts():
    cursor = db_mongo.posts.find({}, {"_id": 0})
    posts = await cursor.to_list(length=100)
    return posts


# ── Route 2 : utilisateurs MySQL ─────────────────────────────────────────────
@app.get("/users")
async def get_users():
    async with mysql_pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM utilisateurs")
            users = await cur.fetchall()
    return list(users)


# ── Healthcheck : vérifie les deux bases ──────────────────────────────────────
@app.get("/health")
async def health():
    errors = []

    # Vérifie MongoDB : la collection posts doit contenir des articles
    try:
        count = await db_mongo.posts.count_documents({})
        if count == 0:
            errors.append("MongoDB: la collection posts est vide")
    except Exception as exc:
        errors.append(f"MongoDB: {exc}")

    # Vérifie MySQL : la table utilisateurs doit contenir des entrées
    try:
        async with mysql_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT COUNT(*) FROM utilisateurs")
                (count,) = await cur.fetchone()
                if count == 0:
                    errors.append("MySQL: la table utilisateurs est vide")
    except Exception as exc:
        errors.append(f"MySQL: {exc}")

    if errors:
        raise HTTPException(status_code=503, detail=errors)

    return {"status": "ok"}
