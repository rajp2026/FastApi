from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken


def create_refresh_token_record(
    db: Session,
    token_hash: str,
    user_id: int,
    expires_at
):
    db_token = RefreshToken(
        token_hash=token_hash,
        user_id=user_id,
        expires_at=expires_at,
    )

    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return db_token


def get_refresh_token_by_hash(db: Session, token_hash: str):
    return db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash,
        RefreshToken.revoked == False
    ).first()


def revoke_refresh_token(db: Session, token_hash: str):
    token = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash
    ).first()

    if token:
        token.revoked = True
        db.commit()

    return token