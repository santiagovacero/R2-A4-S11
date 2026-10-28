from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from modelos import (
    Categoria,
    Producto,
    Movimiento,
    Inventario
)

from estructuras import ListaEnlazada, ListaCircular

from database import (
    SessionLocal,
    ProductoDB,
    MovimientoDB
)


app = Flask(
    __name__,
    template_folder="frontend",
    static_folder="frontend",
    static_url_path=""
)

CORS(app)


inventario = Inventario()


# ==========================================
# CATEGORÍAS
# ==========================================

categoria_frenos = Categoria(
    "Frenos",
    "Pastillas, discos y componentes de freno"
)

categoria_motor = Categoria(
    "Motor",
    "Repuestos y componentes del motor"
)

categoria_transmision = Categoria(
    "Transmisión",
    "Cadenas, piñones y componentes de transmisión"
)

categoria_otros = Categoria(
    "Otros",
    "Otros repuestos y accesorios para motocicletas"
)


# ==========================================
# ESTRUCTURAS DE DATOS
# ==========================================

historial_movimientos = ListaEnlazada()

rotacion_productos = ListaCircular()


# ==========================================
# CARGAR PRODUCTOS DE LA BASE DE DATOS
# ==========================================

def cargar_productos():

    session = SessionLocal()

    productos_db = session.query(
        ProductoDB
    ).all()

    for producto_db in productos_db:

        if producto_db.categoria == "Frenos":

            categoria = categoria_frenos

        elif producto_db.categoria == "Motor":

            categoria = categoria_motor

        elif producto_db.categoria == "Transmisión":

            categoria = categoria_transmision

        else:

            categoria = categoria_otros


        producto = Producto(
            producto_db.nombre,
            producto_db.precio,
            producto_db.stock,
            categoria
        )


        inventario.agregar_producto(
            producto
        )


        rotacion_productos.agregar(
            producto.nombre
        )


    session.close()


# ==========================================
# CREAR PRODUCTOS INICIALES
# ==========================================

def crear_productos_iniciales():

    session = SessionLocal()

    cantidad = session.query(
        ProductoDB
    ).count()


    if cantidad == 0:

        productos = [

            ProductoDB(
                nombre="Pastillas de freno delanteras",
                precio=45000,
                stock=15,
                categoria="Frenos"
            ),

            ProductoDB(
                nombre="Filtro de aceite",
                precio=28000,
                stock=20,
                categoria="Motor"
            ),

            ProductoDB(
                nombre="Kit de arrastre",
                precio=185000,
                stock=8,
                categoria="Transmisión"
            ),

            ProductoDB(
                nombre="Espejos universales",
                precio=35000,
                stock=12,
                categoria="Otros"
            )

        ]


        session.add_all(
            productos
        )

        session.commit()


    session.close()


crear_productos_iniciales()

cargar_productos()


# ==========================================
# PÁGINA PRINCIPAL
# ==========================================

@app.route("/")
def inicio():

    return render_template(
        "index.html"
    )


# ==========================================
# OBTENER PRODUCTOS
# ==========================================

@app.route(
    "/api/productos",
    methods=["GET"]
)
def obtener_productos():

    return jsonify(
        inventario.listar_productos()
    )


# ==========================================
# BUSCAR PRODUCTO
# ==========================================

@app.route(
    "/api/productos/<string:nombre>",
    methods=["GET"]
)
def obtener_producto(nombre):

    producto = inventario.buscar_producto(
        nombre
    )


    if producto is None:

        return jsonify({
            "error": "Repuesto no encontrado"
        }), 404


    return jsonify(
        producto.mostrar_info()
    )


# ==========================================
# ELIMINAR REPUESTO
# ==========================================

@app.route(
    "/api/productos/<string:nombre>",
    methods=["DELETE"]
)
def eliminar_producto(nombre):

    producto = inventario.buscar_producto(
        nombre
    )


    if producto is None:

        return jsonify({
            "error": "Repuesto no encontrado"
        }), 404


    inventario.eliminar_producto(
        nombre
    )


    session = SessionLocal()

    producto_db = session.query(
        ProductoDB
    ).filter_by(
        nombre=nombre
    ).first()


    if producto_db:

        session.delete(
            producto_db
        )

        session.commit()


    session.close()


    return jsonify({

        "mensaje":
        "Repuesto eliminado correctamente"

    })


# ==========================================
# CREAR REPUESTO
# ==========================================

@app.route(
    "/api/productos",
    methods=["POST"]
)
def crear_producto():

    datos = request.json


    nombre = datos.get(
        "nombre"
    )


    precio = float(
        datos.get("precio")
    )


    stock = int(
        datos.get("stock")
    )


    tipo = datos.get(
        "tipo"
    )


    if tipo == "frenos":

        categoria = categoria_frenos

    elif tipo == "motor":

        categoria = categoria_motor

    elif tipo == "transmision":

        categoria = categoria_transmision

    elif tipo == "otros":

        categoria = categoria_otros

    else:

        return jsonify({
            "error": "Categoría no válida"
        }), 400


    producto = Producto(
        nombre,
        precio,
        stock,
        categoria
    )


    inventario.agregar_producto(
        producto
    )


    rotacion_productos.agregar(
        nombre
    )


    session = SessionLocal()


    nuevo_producto = ProductoDB(

        nombre=nombre,

        precio=precio,

        stock=stock,

        categoria=categoria.nombre

    )


    session.add(
        nuevo_producto
    )


    session.commit()

    session.close()


    return jsonify({

        "mensaje":
        "Repuesto agregado correctamente",

        "producto":
        producto.mostrar_info()

    }), 201


# ==========================================
# EDITAR REPUESTO
# ==========================================

@app.route(
    "/api/productos/<string:nombre>",
    methods=["PUT"]
)
def editar_producto(nombre):

    producto = inventario.buscar_producto(
        nombre
    )


    if producto is None:

        return jsonify({
            "error": "Repuesto no encontrado"
        }), 404


    datos = request.json


    nuevo_nombre = datos.get(
        "nombre"
    )


    nuevo_precio = float(
        datos.get("precio")
    )


    nuevo_stock = int(
        datos.get("stock")
    )


    nuevo_tipo = datos.get(
        "tipo"
    )


    if nuevo_tipo == "frenos":

        nueva_categoria = categoria_frenos

    elif nuevo_tipo == "motor":

        nueva_categoria = categoria_motor

    elif nuevo_tipo == "transmision":

        nueva_categoria = categoria_transmision

    elif nuevo_tipo == "otros":

        nueva_categoria = categoria_otros

    else:

        return jsonify({
            "error": "Categoría no válida"
        }), 400


    producto.nombre = nuevo_nombre

    producto.precio = nuevo_precio

    producto.stock = nuevo_stock

    producto.categoria = nueva_categoria


    session = SessionLocal()


    producto_db = session.query(
        ProductoDB
    ).filter_by(
        nombre=nombre
    ).first()


    if producto_db is None:

        session.close()

        return jsonify({
            "error":
            "Repuesto no encontrado en la base de datos"
        }), 404


    producto_db.nombre = nuevo_nombre

    producto_db.precio = nuevo_precio

    producto_db.stock = nuevo_stock

    producto_db.categoria = nueva_categoria.nombre


    session.commit()

    session.close()


    return jsonify({

        "mensaje":
        "Repuesto actualizado correctamente",

        "producto":
        producto.mostrar_info()

    })


# ==========================================
# CREAR MOVIMIENTO
# ==========================================

@app.route(
    "/api/movimientos",
    methods=["POST"]
)
def crear_movimiento():

    datos = request.json


    nombre = datos.get(
        "producto"
    )


    tipo = datos.get(
        "tipo"
    )


    cantidad = int(
        datos.get("cantidad")
    )


    producto = inventario.buscar_producto(
        nombre
    )


    if producto is None:

        return jsonify({
            "error": "Repuesto no encontrado"
        }), 404


    movimiento = Movimiento(
        producto,
        tipo,
        cantidad
    )


    if inventario.registrar_movimiento(
        movimiento
    ):

        historial_movimientos.agregar(
            movimiento.mostrar_info()
        )


        session = SessionLocal()


        nuevo_movimiento = MovimientoDB(

            producto=nombre,

            tipo=tipo,

            cantidad=cantidad,

            fecha=movimiento.fecha.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        )


        session.add(
            nuevo_movimiento
        )


        session.commit()

        session.close()


        session = SessionLocal()


        producto_db = session.query(
            ProductoDB
        ).filter_by(
            nombre=nombre
        ).first()


        if producto_db:

            producto_db.stock = producto.stock

            session.commit()


        session.close()


        return jsonify({

            "mensaje":
            "Movimiento registrado correctamente",

            "movimiento":
            movimiento.mostrar_info(),

            "producto":
            producto.mostrar_info()

        }), 201


    return jsonify({

        "error":
        "No se pudo realizar el movimiento"

    }), 400


# ==========================================
# OBTENER MOVIMIENTOS
# ==========================================

@app.route(
    "/api/movimientos",
    methods=["GET"]
)
def obtener_movimientos():

    session = SessionLocal()


    movimientos = session.query(
        MovimientoDB
    ).all()


    resultado = []


    for movimiento in movimientos:

        resultado.append({

            "id": movimiento.id,

            "producto": movimiento.producto,

            "tipo": movimiento.tipo,

            "cantidad": movimiento.cantidad,

            "fecha": movimiento.fecha

        })


    session.close()


    return jsonify(
        resultado
    )


# ==========================================
# ROTACIÓN DE PRODUCTOS
# ==========================================

@app.route(
    "/api/rotacion",
    methods=["GET"]
)
def obtener_rotacion():

    return jsonify(
        rotacion_productos.mostrar()
    )


# ==========================================
# VALOR TOTAL DEL INVENTARIO
# ==========================================

@app.route(
    "/api/inventario/valor",
    methods=["GET"]
)
def valor_inventario():

    return jsonify({

        "valor_total":
        inventario.valor_total_inventario()

    })


# ==========================================
# EJECUTAR SERVIDOR
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )