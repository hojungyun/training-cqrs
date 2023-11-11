from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app_query.db import initialize_mongodb_database, Database
from app_query.models import Product

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database(Product)


@app.get("/products", response_model=list[Product])
async def retrieve_all_products() -> list[Product]:
    events = await db.get_all()
    return events


@app.post("/products")
async def create_product(
        body: Product,
) -> dict:
    await db.create(body)
    return {"message": "Product created successfully"}


@app.on_event("startup")
async def start_db():
    await initialize_mongodb_database()
