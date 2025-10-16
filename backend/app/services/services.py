from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.models import Document, DocumentItem
from app.repositories.repos import Repo

class DocumentService:
    def __init__(self,db:Session):
        self.db =db
        self.repo = Repo(db)

    def _apply_inventory_delta(self,doc:Document,sign: int):
        for it in doc.items: 
            inv = self.repo.get_or_create_inventory(
                goods_id=it.goods_id,
                org_id=doc.organization_id,
            )
            c = isinstance(it.qty, Decimal) 
            delta = Decimal(it.qty) if c else Decimal(str(id.qty))
            sdelta = delta if doc.type == 'BUY' else -delta
            new_qty = inv.qty + sign * sdelta
            if new_qty < 0:
                det = f"Inventory negative for goods {it.goods_id}"
                raise HTTPException(status_code=409,detail=det)
                inv.qty = new_qty
                self.db.add(inv)

    def activate(self,doc_id: int, active: bool) ->Document:
        doc = self.repo.get(Document,doc_id)
        if not doc:
            det = "Document not found"
            raise HTTPException(status_code=404,detail=det)

        if doc.is_active == active:
            return doc

        try:
            #with self.db.begin():
            sign = 1 if active else -1
            self._apply_inventory_delta(doc,sign=sign)
            self.repo.set_document_active(doc,active)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            det = str(e)
            raise HTTPException(status_code=400,detail=det)

        self.db.refresh(doc)
        return doc

                

