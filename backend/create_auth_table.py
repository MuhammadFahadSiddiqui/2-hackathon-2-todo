"""Create user_auth table for authentication."""
from sqlalchemy import text
from app.database import engine

def create_auth_table():
    """Create user_auth table with proper schema."""
    with engine.connect() as conn:
        # Drop existing user_auth table if it exists
        print("Dropping existing user_auth table if it exists...")
        conn.execute(text("DROP TABLE IF EXISTS user_auth CASCADE"))
        conn.commit()

        # Create user_auth table
        print("Creating user_auth table...")
        conn.execute(text("""
            CREATE TABLE user_auth (
                id VARCHAR(36) PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                name VARCHAR(255),
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """))

        # Create index on email for faster lookups
        conn.execute(text("CREATE INDEX idx_user_auth_email ON user_auth(email)"))
        conn.commit()

        print("✓ user_auth table created successfully")

        # Verify
        result = conn.execute(text("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'user_auth'
            ORDER BY ordinal_position
        """))

        print("\nTable schema:")
        for row in result:
            print(f"  {row[0]:20} {row[1]}")

if __name__ == "__main__":
    create_auth_table()
    print("\n✅ Authentication table setup complete!")
