import os
from sqlalchemy import text
from database import engine

def run_migration():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE reports ADD COLUMN IF NOT EXISTS wpm FLOAT DEFAULT 0.0;"))
            conn.commit()
            print("Successfully mutated `reports` table to include `wpm` column.")
        except Exception as e:
            print(f"Migration error (already exists or other): {e}")

if __name__ == "__main__":
    run_migration()
