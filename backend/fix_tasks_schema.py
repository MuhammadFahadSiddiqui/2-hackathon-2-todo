"""Fix tasks table schema to match the Task model."""
from sqlalchemy import text
from app.database import engine

def fix_tasks_schema():
    """Recreate tasks table with correct schema."""
    with engine.connect() as conn:
        # Drop old tasks table
        print("Dropping old tasks table...")
        conn.execute(text("DROP TABLE IF EXISTS tasks CASCADE"))
        conn.commit()

        # Create tasks table with correct schema
        print("Creating tasks table with correct schema...")
        conn.execute(text("""
            CREATE TABLE tasks (
                id SERIAL PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                is_completed BOOLEAN DEFAULT false,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW(),
                deadline_at TIMESTAMP,
                reminder_interval_minutes INTEGER,
                last_reminded_at TIMESTAMP
            )
        """))

        # Create indexes
        conn.execute(text("CREATE INDEX idx_tasks_user_id ON tasks(user_id)"))
        conn.execute(text("CREATE INDEX idx_tasks_is_completed ON tasks(is_completed)"))
        conn.commit()

        print("✓ Tasks table recreated successfully")

        # Verify
        result = conn.execute(text("""
            SELECT column_name, data_type, column_default
            FROM information_schema.columns
            WHERE table_name = 'tasks'
            ORDER BY ordinal_position
        """))

        print("\nVerified schema:")
        for row in result:
            print(f"  {row[0]:30} {row[1]:30} {row[2]}")

if __name__ == "__main__":
    fix_tasks_schema()
    print("\n✅ Tasks table schema fixed!")
