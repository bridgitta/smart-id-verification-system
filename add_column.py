import sqlite3

conn = sqlite3.connect('database/ids.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE ids ADD COLUMN date_added TEXT")
    print("✅ Column 'date_added' added successfully.")
except Exception as e:
    print("⚠️ Error:", e)

conn.commit()
conn.close()

