# Databases Integration Skill

## Fuente
VoltAgent/awesome-agent-skills (database), ruflo database agents, ComposioHQ/awesome-claude-skills

---

## PostgreSQL

```python
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
from contextlib import contextmanager
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://user:pass@localhost:5432/mydb')

@contextmanager
def get_connection():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

class PostgresDB:
    def __init__(self, url: str = None):
        self.url = url or DATABASE_URL

    def query(self, sql: str, params: tuple = None) -> list[dict]:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params)
                return [dict(row) for row in cur.fetchall()]

    def execute(self, sql: str, params: tuple = None) -> int:
        """Returns number of affected rows."""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.rowcount

    def insert_many(self, table: str, columns: list, values: list[tuple]) -> int:
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES %s"
        with get_connection() as conn:
            with conn.cursor() as cur:
                execute_values(cur, sql, values)
                return cur.rowcount

    def table_exists(self, table: str) -> bool:
        result = self.query(
            "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name=%s)",
            (table,)
        )
        return result[0]['exists']

    def get_schema(self, table: str) -> list[dict]:
        return self.query(
            """SELECT column_name, data_type, is_nullable, column_default
               FROM information_schema.columns
               WHERE table_name = %s ORDER BY ordinal_position""",
            (table,)
        )

# SQLAlchemy (ORM)
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)

Base.metadata.create_all(engine)
```

---

## MySQL / MariaDB

```python
import pymysql
from pymysql.cursors import DictCursor

class MySQLDB:
    def __init__(self, host='localhost', user='root', password='', database='mydb'):
        self.config = {
            'host': host, 'user': user,
            'password': password, 'database': database,
            'cursorclass': DictCursor, 'charset': 'utf8mb4'
        }

    def query(self, sql: str, params: tuple = None) -> list[dict]:
        conn = pymysql.connect(**self.config)
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchall()
        finally:
            conn.close()

    def execute(self, sql: str, params: tuple = None):
        conn = pymysql.connect(**self.config)
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                conn.commit()
                return cur.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
```

---

## SQLite (Local / Embedded)

```python
import sqlite3
from pathlib import Path

class SQLiteDB:
    def __init__(self, db_path: str = "~/.ideas-brillantes/data.db"):
        self.db_path = str(Path(db_path).expanduser())
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")  # Better concurrent access
        conn.execute("PRAGMA foreign_keys=ON")
        conn.close()

    def query(self, sql: str, params: tuple = None) -> list[dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            cur = conn.execute(sql, params or ())
            return [dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def execute(self, sql: str, params: tuple = None) -> int:
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute(sql, params or ())
            conn.commit()
            return cur.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def executemany(self, sql: str, params_list: list[tuple]):
        conn = sqlite3.connect(self.db_path)
        try:
            conn.executemany(sql, params_list)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
```

---

## MongoDB

```python
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.collection import Collection
import os

MONGO_URL = os.environ.get('MONGODB_URL', 'mongodb://localhost:27017')

class MongoDB:
    def __init__(self, database: str, url: str = None):
        self.client = MongoClient(url or MONGO_URL)
        self.db = self.client[database]

    def collection(self, name: str) -> Collection:
        return self.db[name]

    def find(self, collection: str, query: dict = None, 
             projection: dict = None, limit: int = 0) -> list:
        return list(self.db[collection].find(
            query or {}, projection, limit=limit
        ))

    def find_one(self, collection: str, query: dict) -> dict:
        return self.db[collection].find_one(query)

    def insert_one(self, collection: str, document: dict) -> str:
        result = self.db[collection].insert_one(document)
        return str(result.inserted_id)

    def insert_many(self, collection: str, documents: list) -> list:
        result = self.db[collection].insert_many(documents)
        return [str(id) for id in result.inserted_ids]

    def update_one(self, collection: str, query: dict, update: dict):
        return self.db[collection].update_one(query, {'$set': update})

    def delete_one(self, collection: str, query: dict):
        return self.db[collection].delete_one(query)

    def count(self, collection: str, query: dict = None) -> int:
        return self.db[collection].count_documents(query or {})

    def aggregate(self, collection: str, pipeline: list) -> list:
        return list(self.db[collection].aggregate(pipeline))

    def create_index(self, collection: str, fields: list, unique: bool = False):
        index_spec = [(f, ASCENDING) for f in fields]
        self.db[collection].create_index(index_spec, unique=unique)
```

---

## Redis

```python
import redis
import json
from typing import Any, Optional

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def get(self, key: str) -> Optional[Any]:
        value = self.client.get(key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    def set(self, key: str, value: Any, ttl: int = None):
        serialized = json.dumps(value) if not isinstance(value, str) else value
        if ttl:
            self.client.setex(key, ttl, serialized)
        else:
            self.client.set(key, serialized)

    def delete(self, *keys: str):
        self.client.delete(*keys)

    def exists(self, key: str) -> bool:
        return bool(self.client.exists(key))

    def keys(self, pattern: str = '*') -> list[str]:
        return self.client.keys(pattern)

    def incr(self, key: str, amount: int = 1) -> int:
        return self.client.incrby(key, amount)

    def lpush(self, key: str, *values):
        self.client.lpush(key, *[json.dumps(v) for v in values])

    def lrange(self, key: str, start: int = 0, end: int = -1) -> list:
        return [json.loads(v) for v in self.client.lrange(key, start, end)]

    def hset(self, name: str, mapping: dict):
        self.client.hset(name, mapping={k: json.dumps(v) for k, v in mapping.items()})

    def hgetall(self, name: str) -> dict:
        data = self.client.hgetall(name)
        return {k: json.loads(v) for k, v in data.items()}

    def publish(self, channel: str, message: Any):
        self.client.publish(channel, json.dumps(message))

    def subscribe(self, channel: str):
        pubsub = self.client.pubsub()
        pubsub.subscribe(channel)
        return pubsub
```

---

## Supabase (PostgreSQL + Auth + Storage)

```python
from supabase import create_client, Client
import os

supabase: Client = create_client(
    os.environ['SUPABASE_URL'],
    os.environ['SUPABASE_KEY']
)

class SupabaseDB:
    def __init__(self):
        self.db = supabase

    def select(self, table: str, columns: str = '*', 
               filters: dict = None, limit: int = 100) -> list:
        query = self.db.table(table).select(columns)
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        return query.limit(limit).execute().data

    def insert(self, table: str, data: dict | list) -> dict:
        return self.db.table(table).insert(data).execute().data

    def update(self, table: str, data: dict, match: dict) -> dict:
        query = self.db.table(table).update(data)
        for key, value in match.items():
            query = query.eq(key, value)
        return query.execute().data

    def delete(self, table: str, match: dict):
        query = self.db.table(table).delete()
        for key, value in match.items():
            query = query.eq(key, value)
        return query.execute()

    def upload_file(self, bucket: str, path: str, file_data: bytes) -> str:
        self.db.storage.from_(bucket).upload(path, file_data)
        return self.db.storage.from_(bucket).get_public_url(path)

    def rpc(self, function_name: str, params: dict = None):
        return self.db.rpc(function_name, params or {}).execute().data
```

---

## Database Migrations

```python
# Usando alembic para PostgreSQL/SQLAlchemy
# Inicializar: alembic init alembic
# Crear migración: alembic revision --autogenerate -m "add users table"
# Ejecutar: alembic upgrade head
# Revertir: alembic downgrade -1

# Migración manual simple
MIGRATIONS = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """,
    """
    ALTER TABLE users ADD COLUMN IF NOT EXISTS name VARCHAR(255);
    """,
    """
    CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users(email);
    """
]

def run_migrations(db: PostgresDB):
    db.execute("""
        CREATE TABLE IF NOT EXISTS _migrations (
            id SERIAL PRIMARY KEY,
            version INTEGER UNIQUE NOT NULL,
            applied_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    
    applied = {r['version'] for r in db.query("SELECT version FROM _migrations")}
    
    for i, migration in enumerate(MIGRATIONS):
        if i not in applied:
            db.execute(migration)
            db.execute("INSERT INTO _migrations (version) VALUES (%s)", (i,))
            print(f"✅ Migration {i} applied")
```
