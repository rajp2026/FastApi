from app.core.celery_app import celery_app
import time
import random


@celery_app.task(
    bind=True,
    autoretry_for = (Exception,),
    retry_backoff = True,
    retry_backoff_max = True,
    retry_jitter = True,
    retry_max = 3

)
def product_created_task(self, product_id: int, product_name: str):
    print(f"Processing product {product_id}")
    
    #simulates random failure
    if random.choices([True, False]):
        print("simulated failure. retyring ...")
        raise Exception("random failure occured")
    time.sleep(5)
    print(f"Product {product_name} processed by Celery worker")



