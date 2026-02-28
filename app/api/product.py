from fastapi import APIRouter, Depends, Header, HTTPException, Response
from sqlalchemy.orm import Session

from app.models.product import Product
from app.db.database import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_services import ProductService

from app.auth.dependencies import require_permission


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
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("product:create"))

):
    return ProductService.create_product(db, product)

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