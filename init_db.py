import sqlite3

# Connect (or create) the database file
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Drop the table if it already exists
cursor.execute("DROP TABLE IF EXISTS records")

# Create the records table
cursor.execute('''
CREATE TABLE records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    id_number TEXT NOT NULL,
    mother_name TEXT,
    father_name TEXT,
    place_of_birth TEXT,
    status TEXT,
    submission_date TEXT
)
''')

# Insert some sample validated records
sample_data = [
    ('Alice Smith', 'ID12345', 'Jane Smith', 'John Smith', 'Nairobi', 'Validated', '2025-04-01'),
    ('Bob Johnson', 'ID67890', 'Mary Johnson', 'David Johnson', 'Kampala', 'Validated', '2025-04-10'),
    ('Charlie Brown', 'ID11122', 'Nancy Brown', 'Peter Brown', 'Mombasa', 'Archived', '2025-04-05'),
]

cursor.executemany('''
INSERT INTO records (name, id_number, mother_name, father_name, place_of_birth, status, submission_date)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', sample_data)

conn.commit()
conn.close()

print("✅ Database and records table created successfully.")
