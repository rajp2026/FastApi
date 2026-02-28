from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import StaleDataError
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from fastapi import Header, HTTPException

class ProductService:

    @staticmethod
    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Product:
        try:
            # makeing prodcut model object ** helps to make it indit dict
            db_product = Product(**product_data.model_dump())

            db.add(db_product)
            db.commit()
            db.refresh(db_product)

            return db_product

        except SQLAlchemyError as e:
            db.rollback()
            raise e
    

    # @staticmethod
    # def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> Product:
    #    # this is below is updaitng the product direclty into db like bulck update thousands of rows at once
    # #       db.query(Product).filter(Product.category == "Electronics").update({
    # #       "is_available": False,
    # #       "updated_at": func.now()
    # #        })
    # #       db.commit()
       
    #     db_product = db.query(Product).filter(Product.id == product_id).first()

    #     if not db_product:
    #         raise HTTPException(status_code = 404, detail="product not found")

    #     update_data = product_data.model_dump(exclude_unset=True) # ecclue_unset provetns overirind of fiels with none

    #     for key, value in update_data.items():
    #         setattr(db_product, key, value)

    #     db.commit()
    #     db.refresh(db_product)

    #     return db_product



    # below update method with version in header to handle the conflict at 
    # at db when at same time user try to update same record in db
    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_data: ProductUpdate,
        client_version: int
    ) -> Product:
               
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        # Version check (HTTP-agnostic)
        if product.version != client_version:
            raise HTTPException(
                status_code=412,
                detail="Resource modified by another user"
            )

        update_data = product_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        try:
            db.commit()
        except StaleDataError:
            db.rollback()
            raise HTTPException(
                status_code=412,
                detail="Conflict detected during update"
            )

        db.refresh(product)

        return product