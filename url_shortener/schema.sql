CREATE TABLE IF NOT EXISTS shortener (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_url TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)