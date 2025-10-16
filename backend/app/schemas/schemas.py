from datetime import date
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Literal

class OrganizationCreate(BaseModel):
    name: str

class OrganizationRead(OrganizationCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CustomerCreate(BaseModel):
    name: str

class CustomerRead(CustomerCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CurrencyCreate(BaseModel):
    code: str = Field(min_length=3, max_length=3)

class CurrencyRead(CurrencyCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
    
class GoodsCreate(BaseModel):
    sku: str
    name: str

class GoodsRead(GoodsCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class DocumentItemCreate(BaseModel):
    goods_id: int
    price: float
    qty: float

class DocumentItemRead(DocumentItemCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class DocumentCreate(BaseModel):
    doc_num: str
    doc_date: date
    type:  Literal['SELL','BUY']
    organization_id: int
    customer_id: int
    currency_id: int
    items: List[DocumentItemCreate]
    
class DocumentRead(BaseModel):
    id: int
    doc_num: str
    doc_date: date
    type: str
    organization_id: int
    customer_id: int
    currency_id: int
    is_active: bool
    items: List[DocumentItemRead]
    model_config = ConfigDict(from_attributes=True)

class ActivatePayload(BaseModel):
    active: bool


    



    




