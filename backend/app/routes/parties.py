from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.models import Organization, Customer, Currency
from app.schemas.schemas import OrganizationCreate,OrganizationRead
from app.schemas.schemas import CustomerCreate,CustomerRead
from app.schemas.schemas import CurrencyCreate,CurrencyRead

router = APIRouter(prefix="/api/parties",tags=["parties"])

@router.post(
    "/organizations",
    response_model=OrganizationRead,
)
def create_org(
    payload: OrganizationCreate,
    db: Session = Depends(get_db),
):
    org = Organization(name=payload.name)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org

@router.get(
    "/organizations",
    response_model=list[OrganizationRead],
)
def list_orgs(
    db: Session = Depends(get_db),
):
    return db.query(Organization).all()

@router.post(
    "/customers",
    response_model=CustomerRead,
)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
):
    c = Customer(name = payload.name)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.get(
    "/customers",
    response_model=list[CustomerRead],
)
def list_customers(
    db: Session = Depends(get_db),
):
    return db.query(Customer).all()

@router.post(
    "/currencies",
    response_model=CurrencyRead,
)
def create_currency(
    payload: CurrencyCreate,
    db: Session = Depends(get_db),
):
    cur = Currency(code=payload.code.upper())
    db.add(cur)
    db.commit()
    db.refresh(cur)
    return c

@router.get(
    "/currencies",
    response_model=list[CurrencyRead],
)
def list_currencies(
    db: Session = Depends(get_db),
):
    return db.query(Currency).all()

    





