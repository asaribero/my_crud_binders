from mcp.server.fastmcp import FastMCP
import sqlite3
from database import init_db

# Inicializar la BD
init_db()

# Instanciar MCP
mcp = FastMCP("ReaseguroDB")
DB = "binders.db"

@mcp.tool()
def crear_binder(
    reasegurador: str,
    tipo: str,
    limite: float,
    fecha_inicio: str,
    fecha_fin: str
) -> str:
    conn = sqlite3.connect(DB)
    cur  = conn.cursor()
    cur.execute("""
        INSERT INTO binders
            (reasegurador, tipo, limite, fecha_inicio, fecha_fin)
        VALUES (?, ?, ?, ?, ?)
    """, (reasegurador, tipo, limite, fecha_inicio, fecha_fin))
    conn.commit()
    conn.close()
    return "Binder creado exitosamente"

@mcp.tool()
def consultar_binder(binder_id: int) -> dict:
    conn = sqlite3.connect(DB)
    cur  = conn.cursor()
    cur.execute("SELECT * FROM binders WHERE binder_id = ?", (binder_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "binder_id":    row[0],
            "reasegurador": row[1],
            "tipo":         row[2],
            "limite":       row[3],
            "fecha_inicio": row[4],
            "fecha_fin":    row[5],
        }
    return {"error": "Binder no encontrado"}

@mcp.tool()
def actualizar_binder(
    binder_id: int,
    limite: float = None,
    fecha_fin: str = None
) -> str:
    conn = sqlite3.connect(DB)
    cur  = conn.cursor()
    if limite is not None:
        cur.execute(
            "UPDATE binders SET limite = ? WHERE binder_id = ?",
            (limite, binder_id)
        )
    if fecha_fin is not None:
        cur.execute(
            "UPDATE binders SET fecha_fin = ? WHERE binder_id = ?",
            (fecha_fin, binder_id)
        )
    conn.commit()
    conn.close()
    return "Binder actualizado correctamente"

@mcp.tool()
def eliminar_binder(binder_id: int) -> str:
    conn = sqlite3.connect(DB)
    cur  = conn.cursor()
    cur.execute("DELETE FROM binders WHERE binder_id = ?", (binder_id,))
    conn.commit()
    conn.close()
    return "Binder eliminado correctamente"

@mcp.tool()
def listar_binders() -> dict:
    conn = sqlite3.connect(DB)
    cur  = conn.cursor()
    cur.execute("SELECT * FROM binders")
    rows = cur.fetchall()
    conn.close()
    return {
        row[0]: {
            "reasegurador": row[1],
            "tipo":         row[2],
            "limite":       row[3],
            "fecha_inicio": row[4],
            "fecha_fin":    row[5],
        }
        for row in rows
    }

if __name__ == "__main__":
    # Inicia el servidor usando el transport y puerto por defecto (stdio)
    mcp.run()
