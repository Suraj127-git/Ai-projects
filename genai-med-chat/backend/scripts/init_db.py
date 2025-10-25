# backend/scripts/init_db.py
"""
Initializes MySQL tables via SQLAlchemy metadata (simple).
Run after MySQL is available.
"""
from app.repos.mysql_repo import metadata, engine

def main():
    print("Creating tables (if not exist)...")
    metadata.create_all(engine)
    print("Done.")

if __name__ == "__main__":
    main()
