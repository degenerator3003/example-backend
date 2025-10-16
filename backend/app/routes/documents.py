from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.models import Document, DocumentItem
from app.schemas.schemas import DocumentCreate, DocumentRead
from app.schemas.schemas import ActivatePayload
from app.services.services import DocumentService

router = APIRouter(
    prefix = "/api/documents",
    tags=["documents"],
)

@router.post(
   "/",
   response_model=DocumentRead,
)
def create_document(
    payload: DocumentCreate,
    db: Session = Depends(get_db),
):
    doc = Document(
        doc_num=payload.doc_num,
        doc_date=payload.doc_date,
        type=payload.type,
        organization_id=payload.organization_id,
        customer_id=payload.customer_id,
        currency_id=payload.currency_id,
    )
    for it in payload.items:
        new_itemdoc = DocumentItem(
            goods_id = it.goods_id,
            price = it.price,
            qty = it.qty,
        )
        doc.items.append(new_itemdoc)

    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

@router.get(
    "/",
    response_model=list[DocumentRead],
)
def list_documents(
    db: Session = Depends(get_db),
):
    return db.query(Document).all()

@router.post(
    "/{doc_id}/activate",
    response_model=DocumentRead
)
def activate_document(
    doc_id: int,
    payload: ActivatePayload,
    db: Session = Depends(get_db),
):
    svc = DocumentService(db)
    doc = svc.activate(doc_id,active = payload.active)
    return doc



