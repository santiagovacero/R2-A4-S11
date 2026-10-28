
import sqlite3
from pathlib import Path

from database import SessionLocal, ProductoDB, MovimientoDB


# Ubicar la base SQLite en esta misma carpeta
ruta_sqlite = Path(__file__).with_name("inventario.db")

conexion = sqlite3.connect(ruta_sqlite)
conexion.row_factory = sqlite3.Row

sesion = SessionLocal()

try:
    # Leer los datos originales
    productos = conexion.execute(
        "SELECT id, nombre, precio, stock, categoria FROM productos"
    ).fetchall()

    movimientos = conexion.execute(
        "SELECT id, producto, tipo, cantidad, fecha FROM movimientos"
    ).fetchall()

    print("Productos encontrados en SQLite:", len(productos))
    print("Movimientos encontrados en SQLite:", len(movimientos))

    # Evitar duplicados: no migrar si MySQL ya contiene registros
    if sesion.query(ProductoDB).count() > 0:
        raise RuntimeError(
            "MySQL ya contiene productos. Se cancela para evitar duplicados."
        )

    if sesion.query(MovimientoDB).count() > 0:
        raise RuntimeError(
            "MySQL ya contiene movimientos. Se cancela para evitar duplicados."
        )

    # Copiar productos conservando sus IDs
    for fila in productos:
        sesion.add(
            ProductoDB(
                id=fila["id"],
                nombre=fila["nombre"],
                precio=fila["precio"],
                stock=fila["stock"],
                categoria=fila["categoria"]
            )
        )

    # Copiar movimientos conservando sus IDs
    for fila in movimientos:
        sesion.add(
            MovimientoDB(
                id=fila["id"],
                producto=fila["producto"],
                tipo=fila["tipo"],
                cantidad=fila["cantidad"],
                fecha=fila["fecha"]
            )
        )

    sesion.commit()

    print("¡Migración completada correctamente!")
    print("Productos copiados:", len(productos))
    print("Movimientos copiados:", len(movimientos))

except Exception:
    sesion.rollback()
    raise

finally:
    sesion.close()
    conexion.close()
