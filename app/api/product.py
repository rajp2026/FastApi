from fastapi import APIRouter, Depends, Header, HTTPException, Response, BackgroundTasks
from sqlalchemy.orm import Session

from app.models.product import Product
from app.db.database import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_services import ProductService

from app.auth.dependencies import require_permission
from app.services.product_tasks import product_created_notification
from app.task_queue.product_task import product_created_task

from celery.result import AsyncResult
from app.core.celery_app import celery_app

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/", response_model = list[ProductResponse])
def get_all_products(
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("product:read"))
):
    product = db.query(Product).all()
    return product


@router.post("/create", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    # background_tasks : BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("product:create"))

):  
    db_product = ProductService.create_product(db, product)

    #add background task here
    # background_tasks.add_task(
    #     product_created_notification,
    #     db_product.id,
    #     db_product.name
    #     ) 
        # 🔥 Push task to Redis
    task = product_created_task.delay(
        db_product.id,
        db_product.name
    )

    # return db_product 
    return {
        "product_id": db_product.id,
        "task_id": task.id
    }

 #// adding another oruter to get taskid which we will use in celery for monitoring   
@router.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }


# @router.patch("/{product_id}/update")
# def update_product(
#     product_id: int,
#     product_data: ProductUpdate,
#     db: Session = Depends(get_db)
# ):
#     return ProductService.update_product(db, product_id, product_data)



@router.patch("/{product_id}/update", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    if_match: str = Header(None),
    db: Session = Depends(get_db),
    response: Response = None
):
    breakpoint()
    if not if_match:
        raise HTTPException(
            status_code=400,
            detail="If-Match header required"
        )

    # Expecting format: "v3"
    try:
        client_version = int(if_match.replace('"v', '').replace('"', ''))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ETag format")

    updated_product = ProductService.update_product(
        db=db,
        product_id=product_id,
        product_data=product_data,
        client_version=client_version
    )

    # Return new ETag after successful update
    response.headers["ETag"] = f'"v{updated_product.version}"'

    return updated_product