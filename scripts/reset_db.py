from app import app, db
from seed_data import seed_database

if __name__ == "__main__":
    with app.app_context():
        # Drop everything, recreate schema
        db.drop_all()
        db.create_all()
        # Optional: reseed with sample data
        seed_database()
        print("Database reset and reseeded.")