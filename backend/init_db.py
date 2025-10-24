#init_db.py - Script to initialize the database by dropping and creating all tables

from database import engine, Base
import models

if __name__ == "__main__":
    print("--- WARNING: This will delete all existing data in your tables. ---")
    print("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating all database tables...")
    Base.metadata.create_all(bind=engine)
    
    print("✓ Database tables created successfully!")