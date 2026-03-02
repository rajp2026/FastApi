import time


def product_created_notification(product_id: int, product_name: str,):
    print(f"Starting background task for product {product_id}")
    time.sleep(5)  # simulate heavy work 
    print(f"product {product_name} proccessed in background")

