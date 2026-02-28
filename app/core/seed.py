from sqlalchemy.orm import Session
from app.models.role import Role
from app.models.permission import Permission
from app.core.constants import ROLE_PERMISSION_MAP

from app.models.user import User
from app.core.security import hash_password

def seed_permissions(db: Session):
    permissions = [
        "product:create",
        "product:read",
        "product:update",
        "product:delete",
        "user:create",
        "user:read",
    ]

    for perm_name in permissions:
        exists = db.query(Permission).filter_by(name=perm_name).first()
        if not exists:
            db.add(Permission(name=perm_name))

    db.commit()


def seed_roles(db: Session):
    for role_name in ["admin", "user"]:
        exists = db.query(Role).filter_by(name=role_name).first()
        if not exists:
            db.add(Role(name=role_name))

    db.commit()


# def assign_permissions(db: Session):
#     admin = db.query(Role).filter_by(name="admin").first()
#     user = db.query(Role).filter_by(name="user").first()

#     all_permissions = db.query(Permission).all()

#     # Admin gets everything
#     admin.permissions = all_permissions

#     # User gets limited permissions
#     user_permissions = db.query(Permission).filter(
#         Permission.name.in_([
#             "product:create",
#             "product:read"
#         ])
#     ).all()

#     user.permissions = user_permissions

#     db.commit()
def assign_permissions(db: Session):
    for role_name, permissions in ROLE_PERMISSION_MAP.items():
        role = db.query(Role).filter_by(name=role_name).first()
        if not role:
            continue

        # If role gets all permissions
        if permissions == "*":
            role.permissions = db.query(Permission).all()
        else:
            role.permissions = db.query(Permission).filter(
                Permission.name.in_(permissions)
            ).all()

    db.commit()

def seed_admin_user(db: Session):
    from app.models.role import Role
    from app.models.user import User

    admin_email = "admin@gmail.com"

    existing_admin = db.query(User).filter_by(email=admin_email).first()
    if existing_admin:
        return

    admin_role = db.query(Role).filter_by(name="admin").first()

    admin_user = User(
        email=admin_email,
        hashed_password=hash_password("admin"),
        role=admin_role
    )

    db.add(admin_user)
    db.commit()

def seed_database(db: Session):
    seed_permissions(db)
    seed_roles(db)
    assign_permissions(db)
    seed_admin_user(db)