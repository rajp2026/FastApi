from app.db.database import SessionLocal
from app.core.seed import seed_database
breakpoint()

def run():
    db = SessionLocal()
    try:
        seed_database(db)
        print("Database seeded successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    run()