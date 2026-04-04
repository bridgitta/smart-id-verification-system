-- SQLite command
CREATE TABLE ids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_number TEXT UNIQUE NOT NULL,
    name TEXT,
    dob TEXT,
    father TEXT,
    mother TEXT,
    place TEXT  
);
