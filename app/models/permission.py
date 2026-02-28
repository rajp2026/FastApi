# database modeling (rbac core)
# we are going to implment 
# User -> Role -> Permissions

# this means one user has one role (for now)
# one role has many permissions
# One permission can belong to many roles

from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String, unique=True, nullable=False)
    ####
    # each row represent a permission like:
    # product:create
    #product:update
    