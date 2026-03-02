from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.task_queue.product_task"]  # 👈 ADD THIS
    
)

celery_app.conf.update(
    task_serializer = "json",
    accept_content = ["json"],
    result_serializer = "json",
    timezone = "UTC",
    enable_utc = True,
)

celery_app.autodiscover_tasks(["app.task_queue"])
