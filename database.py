import sqlite3

def init_db():
    conn = sqlite3.connect("binders.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS binders (
        binder_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        reasegurador TEXT    NOT NULL,
        tipo         TEXT,
        limite       REAL,
        fecha_inicio TEXT,
        fecha_fin    TEXT
    )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Base de datos 'binders.db' inicializada con tabla 'binders'.")
