from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.models import (
    Organization,
    Customer,
    Currency,
    Goods,
    Inventory,
    Document,
    DocumentItem,
)

class Repo:
    def __init__(self,db:Session):
        self.db = db

    def get(self,model,id_:int):
        return self.db.get(model,id_)

    def list(self,model):
        return self.db.execute(select(model)).scalars().all()

    def add(self,obj):
        self.db.add(obj)
        return obj

    def get_or_create_inventory(self,goods_id: int,org_id:int) -> Inventory: 
        sel = select(Inventory).where(Inventory.goods_id == goods_id,Inventory.organization_id == org_id)
        inv = self.db.execute(sel).scalar_one_or_none()
        if inv is None:
            inv = Inventory(goods_id=goods_id,organization_id=org_id,qty=0)
            self.db.add(inv)
            self.db.flush()
        return inv

    def create_document(self, doc: Document) -> Document:
        self.db.add(doc)
        self.db.flush()
        return doc

    def set_document_active(self,doc:Document,active: bool):
        doc.is_active = active
        self.db.add(doc)
    



