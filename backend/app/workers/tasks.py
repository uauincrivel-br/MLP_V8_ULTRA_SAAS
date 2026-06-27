
from backend.app.workers.celery_app import celery
from backend.app.database import SessionLocal
from backend.app.models.models import Product, Job
from backend.app.services.event_bus import publish_event
import requests

def update_job(job, stage):
    job.stage = stage
    job.status = "processing"
    publish_event("jobs", {"job_id": job.id, "stage": stage})

@celery.task(bind=True)
def process_product(self, job_id: int):

    db = SessionLocal()

    job = db.query(Job).filter(Job.id == job_id).first()
    product = db.query(Product).filter(Product.id == job.product_id).first()

    if not job or not product:
        return

    update_job(job, "enrich")
    db.commit()

    update_job(job, "publish")
    db.commit()

    try:
        resp = requests.post(
            "https://api.mercadolibre.com/items",
            json={
                "title": product.title,
                "price": product.price,
                "available_quantity": product.stock
            },
            timeout=30
        )

        if resp.status_code >= 300:
            raise Exception(resp.text)

        data = resp.json()

        product.item_id = data.get("id")
        job.status = "done"
        job.stage = "finished"

        publish_event("jobs", {
            "job_id": job.id,
            "status": "done",
            "item_id": product.item_id
        })

        db.commit()

    except Exception as e:
        job.status = "failed"
        product.error = str(e)
        db.commit()

        publish_event("jobs", {
            "job_id": job.id,
            "status": "failed",
            "error": str(e)
        })
