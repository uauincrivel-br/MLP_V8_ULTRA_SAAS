
from fastapi import FastAPI, WebSocket, UploadFile, File
import pandas as pd
import tempfile
import os
import traceback

from backend.app.database import SessionLocal, Base, engine
from backend.app.models.models import Product, Job
from backend.app.ws.manager import manager
from backend.app.workers.tasks import process_product

app = FastAPI()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.websocket("/ws/jobs")
async def ws_jobs(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except:
        manager.disconnect(ws)


@app.post("/api/import/upload")
def upload(file: UploadFile = File(...)):

    db = SessionLocal()
    path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(file.file.read())
            path = tmp.name

        df = pd.read_excel(path)

        created = 0

        for _, row in df.iterrows():

            product = Product(
                sku=str(row.get("SKU")),
                title=str(row.get("TITLE")),
                price=row.get("PRICE", 0),
                stock=row.get("STOCK", 1),
                status="queued"
            )

            db.add(product)
            db.commit()

            created += 1

        return {"created": created}

    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }

    finally:
        db.close()
        if path and os.path.exists(path):
            os.remove(path)
