from beanie import Document


class Product(Document):
    name: str
    sql_id: int

    class Settings:
        name = "products"
