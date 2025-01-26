import sqlite3

# Database initialization script
DATABASE = "test.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create users table (example)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
    ''')

    # Add a test user (you can customize this)
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('user1', 'password123')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('user2', 'password123')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('guest', 'password123')")

    conn.commit()
    conn.close()
    print("Database initialized!")

if __name__ == "__main__":
    init_db()
