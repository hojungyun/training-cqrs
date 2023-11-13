import orjson
from fastapi import FastAPI, Depends, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from event_bus.mq_conn import AmqpConnection

# MQ
mq = AmqpConnection()
mq.connect()
mq.setup_queues()

# RDBMS
engine = create_engine("sqlite:///db.sqlite3", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# PYDANTIC
class ProductBase(BaseModel):
    name: str


# FASTAPI
app = FastAPI()

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductBase, db: Session = Depends(get_db)):
    db_product = Product(name=product.name)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Send product data to MQ as an alternative to CDC
    product_data: bytes = orjson.dumps({
        "name": db_product.name,
        "sql_id": db_product.id,
    })
    print(f"Sending message to MQ now !!!! {product_data=}")
    mq.publish(payload=product_data)

    return {"ok": True}
