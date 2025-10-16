from sqlalchemy import (Column,Integer,String,Date,Boolean,ForeignKey, Numeric,
UniqueConstraint, CheckConstraint)

from sqlalchemy.orm import relationship
from app.core.db import Base

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer,primary_key=True)
    name = Column(String(200),unique=True,nullable=False)


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer,primary_key=True)
    name = Column(String(200),unique=True,nullable=False)

class Currency(Base):
    __tablename__ = "currencies"
    id = Column(Integer,primary_key=True)
    code = Column(String(3),unique=True,nullable=False)

class Goods(Base):
    __tablename__="goods"
    id = Column(Integer,primary_key=True)
    sku = Column(String(64),unique=True,nullable=False)
    name = Column(String(200),nullable=False)

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer,primary_key=True)
    goods_id_fk = ForeignKey("goods.id",ondelete="RESTRICT")
    goods_id = Column(Integer,goods_id_fk,nullable=False)
    org_fk = ForeignKey("organizations.id",ondelete="RESTRICT")
    organization_id = Column(Integer,org_fk,nullable=False)
    qty = Column(Numeric(18,3),nullable=False,default=0)
    uc = UniqueConstraint("goods_id","organization_id",name="uq_inventory_goods_org")
    cc = CheckConstraint("qty >= 0",name="ck_inventory_nonnegative")
    __table_args__ = (uc,cc,)
    goods = relationship("Goods")
    organization = relationship("Organization")
    

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer,primary_key=True)
    doc_num = Column(String(50),nullable=False)
    doc_date = Column(Date,nullable = False)
    type = Column(String(10),nullable=False)
    org_fk = ForeignKey("organizations.id")
    organization_id = Column(Integer,org_fk,nullable=False)
    cust_fk = ForeignKey("customers.id")
    customer_id = Column(Integer,cust_fk,nullable=False)
    curr_fk = ForeignKey("currencies.id")
    currency_id = Column(Integer,curr_fk,nullable=False)
    is_active = Column(Boolean,nullable=False,default=False)


    organization = relationship("Organization")
    customer = relationship("Customer")
    currency = relationship("Currency")
    items = relationship(
        "DocumentItem",
        cascade="all,delete-orphan",
        back_populates="document",
    )


class DocumentItem(Base):
    __tablename__="document_items"
    id = Column(Integer,primary_key=True)
    doc_fk = ForeignKey("documents.id",ondelete="CASCADE")
    document_id = Column(Integer,doc_fk,nullable=False)
    goods_fk = ForeignKey("goods.id",ondelete="RESTRICT")
    goods_id = Column(Integer,goods_fk,nullable=False)
    price = Column(Numeric(18,2),nullable=False)
    qty = Column(Numeric(18,3),nullable=False)

    goods = relationship("Goods")
    document = relationship("Document",back_populates="items")


