from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from contextlib import asynccontextmanager # type: ignore

from config.db_mysql import test_mysql_connection, init_mysql_tables, seed_mysql_database # type: ignore
from config.db_mongo import test_mongo_connection, init_mongo_collections # type: ignore

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\nIniciando API Híbrida...")
    test_mysql_connection()
    init_mysql_tables()
    seed_mysql_database()
    test_mongo_connection()
    init_mongo_collections()
    yield
    print("\nApagando API Híbrida...")

app = FastAPI(title="Hospital Híbrido MD - API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from tests.nosql.notas import router as nosql_router
app.include_router(nosql_router)

from tests.sql.notas import router as sql_router
app.include_router(sql_router)

@app.get("/")
def home():
    return {"mensaje": "API configurada y corriendo desde la raíz"}

if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
