from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import SessionLocal
from app.models import Product
from app.schemas import ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    """Barcha mahsulotlarni qaytaradi"""
    return db.query(Product).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """ID bo‘yicha bitta mahsulotni qaytaradi"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/search", response_model=List[ProductResponse])
def search_products(
    name: str = Query(...),
    db: Session = Depends(get_db)
):
    """Nom bo‘yicha mahsulotlarni qidiradi"""
    return db.query(Product).filter(Product.name.ilike(f"%{name}%")).all()


@router.get("/filter/category", response_model=List[ProductResponse])
def filter_by_category(
    category: str = Query(...),
    db: Session = Depends(get_db)
):
    """Kategoriya bo‘yicha filterlash"""
    return db.query(Product).filter(Product.category == category).all()


@router.get("/filter/price", response_model=List[ProductResponse])
def filter_by_price(
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Narx oralig‘i bo‘yicha filterlash"""
    query = db.query(Product)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    return query.all()


@router.get("/paginated", response_model=List[ProductResponse])
def get_paginated_products(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Pagination bilan mahsulotlarni qaytaradi"""
    return db.query(Product).limit(limit).offset(offset).all()


@router.get("/in-stock", response_model=List[ProductResponse])
def filter_by_stock(
    status: bool,
    db: Session = Depends(get_db)
):
    """Skladda bor yoki yo‘qligiga qarab filterlash"""
    return db.query(Product).filter(Product.in_stock == status).all()
