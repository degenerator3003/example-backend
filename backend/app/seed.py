from datetime import date
from sqlalchemy import select
from app.core.db import SessionLocal, engine, Base
from app.models.models import Organization, Customer, Currency
from app.models.models import Goods, Inventory, Document, DocumentItem

engine.echo = False 
Base.metadata.create_all(bind=engine)

def get_or_create(session, model, defaults=None, **kwargs):
    sel =select(model).filter_by(**kwargs)
    inst = session.execute(sel).scalar_one_or_none()
    if inst:
        return inst
    params = {**kwargs,**(defaults or {})}
    inst = model(**params)
    session.add(inst)
    session.flush()
    return inst

def run():
    with SessionLocal() as s:
        with s.begin():
            org = get_or_create(s,Organization,name="Acme LLC")
            cust = get_or_create(s,Customer,name="Jonn Doe")
            cur = get_or_create(s,Currency,code="USD")

            g1 = get_or_create(
                s,
                Goods,
                sku="SKU-001",
                defaults={"name":"Wiget A"},
            )
 
            g2 = get_or_create(
                s,
                Goods,
                sku="SKU-002",
                defaults={"name":"Wiget B"},
            )

            for g in (g1,g2):
                sel = select(Inventory).where(
                    Inventory.goods_id==g.id,
                    Inventory.organization_id==org.id,
                )
                inv = s.execute(sel).scalar_one_or_none()
                if not inv:
                    new_g = Inventory(
                        goods_id = g.id,
                        organization_id = org.id,
                        qty = 100,
                    )
                    s.add(new_g)


                seld = select(Document).where(
                    Document.doc_num=="S-1001",
                )
                docs = s.execute(seld).scalars().all() 
                if len(docs) > 1:
                    for d in docs[1:]:
                        s.delete(d)
                    #s.commit()

                exe = s.execute(seld).scalar_one_or_none()

                if not exe:
                    d = Document(
                        doc_num="S-1001",
                        doc_date=date.today(),
                        type='SELL',
                        organization_id=org.id,
                        customer_id=cust.id,
                        currency_id=cur.id
                    )
                    di_1 = DocumentItem(
                        goods_id=g1.id,
                        qty=5,
                        price=10,
                    )
                    d.items.append(di_1)
                    di_2 = DocumentItem(
                        goods_id=g2.id,
                        qty=2,
                        price=20,
                    )
                    d.items.append(di_2)
                    s.add(d)

                seld = select(Document).where(
                    Document.doc_num=="B-1001",
                )
                docs = s.execute(seld).scalars().all() 
                if len(docs) > 1:
                    for d in docs[1:]:
                        s.delete(d)
                    #s.commit()
               
                exe = s.execute(seld).scalar_one_or_none()
                
                if not exe:
                    d = Document(
                        doc_num="B-1001",
                        doc_date=date.today(),
                        type='BUY',
                        organization_id=org.id,
                        customer_id=cust.id,
                        currency_id=cur.id
                    )
                    di_1 = DocumentItem(
                        goods_id=g1.id,
                        qty=50,
                        price=1,
                    )
                    d.items.append(di_1)
                    di_2 = DocumentItem(
                        goods_id=g2.id,
                        qty=200,
                        price=2,
                    )
                    d.items.append(di_2)
                    

if __name__=="__main__":
    run()
    print("Seed completed")








    
   

