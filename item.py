from pydantic import BaseModel


class Item(BaseModel):
    id: int = 0
    address: str = ""
