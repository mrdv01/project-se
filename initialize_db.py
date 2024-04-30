import sqlite3

def get_db():
    conn = sqlite3.connect('hotel.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            room_no INTEGER PRIMARY KEY,
            capacity INTEGER NOT NULL,
            rate REAL NOT NULL,
            occupied BOOLEAN NOT NULL DEFAULT 0,
            guests TEXT
        )
    ''')
    conn.commit()
    conn.close()

def seed_data():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM rooms')
    row_count = c.fetchone()[0]
    if row_count == 0:
        c.execute('''
            INSERT INTO rooms (room_no, capacity, rate, occupied, guests)
            VALUES
                (101, 2, 99.99, 0, NULL),
                (102, 4, 149.99, 1, 'John Doe, Jane Smith'),
                (103, 3, 129.99, 0, NULL),
                (104, 2, 89.99, 1, 'Bob Johnson'),
                (105, 5, 199.99, 0, NULL)
        ''')
        conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    seed_data()
    print("Database initialized and seeded successfully.")