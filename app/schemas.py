from typing import List

from pydantic import BaseModel, Field


class CategoryReponse(BaseModel):
    category_id: int
    name: str = Field(max_length=100)
    description: str | None = None

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str = Field(max_length=100)
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = Field(max_length=100)
    description: str | None = None


class ProductResponse(BaseModel):
    product_id: int
    name: str = Field(max_length=64)
    price: float
    in_stock: bool
    category_id: int

    class Config:
        from_attributes = True
