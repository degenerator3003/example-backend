from fastapi import FastAPI
from app.core.db import Base, engine
from app.routes import parties, goods, documents

app = FastAPI(title="Trade API",version="0.1.0")

Base.metadata.create_all(bind=engine)

app.include_router(parties.router)
app.include_router(goods.router)
app.include_router(documents.router)

@app.get("/")
def root():
    return {"status":"ok","service":"trade-api"}



