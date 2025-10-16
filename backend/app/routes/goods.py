from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.models import Goods, Inventory
from app.schemas.schemas import GoodsCreate, GoodsRead

router = APIRouter(
    prefix="/api/goods",
    tags=["goods"],
)

@router.post(
    "/",
    response_model=GoodsRead,
)
def create_goods(
    payload: GoodsCreate,
    db: Session = Depends(get_db),
):
    g = Goods(sku = payload.sku, name = payload.name)
    db.add(d)
    db.commit()
    db.refresh(g)
    return g

@router.get(
    "/",
    response_model=list[GoodsRead]
)
def list_goods(
    db: Session = Depends(get_db),
):
    return db.query(Goods).all()

@router.get("/inventory")
def list_inventory(db: Session = Depends(get_db)):
    data = db.query(Inventory).all()
    make_item = lambda i: {
        "goods_id": i.goods_id,
        "organization_id": i.organization_id,
        "qty": float(i.qty),
    }
    return [make_item(i) for i in data]




