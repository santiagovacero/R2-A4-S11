from datetime import datetime


# =========================
# CLASE CATEGORIA
# =========================

class Categoria:

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def mostrar_info(self):
        return f"{self.nombre}: {self.descripcion}"


# =========================
# CLASE PROVEEDOR
# =========================

class Proveedor:

    def __init__(self, nombre, telefono, correo):
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo

    def mostrar_info(self):
        return (
            f"Proveedor: {self.nombre} | "
            f"Teléfono: {self.telefono} | "
            f"Correo: {self.correo}"
        )


# =========================
# CLASE PRODUCTO
# =========================

class Producto:

    def __init__(self, nombre, precio, stock, categoria):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria

    def calcular_valor(self):
        return self.precio * self.stock

    def aumentar_stock(self, cantidad):
        self.stock += cantidad

    def disminuir_stock(self, cantidad):

        if cantidad <= self.stock:
            self.stock -= cantidad
            return True

        return False

    def obtener_descripcion(self):
        return f"Producto: {self.nombre}"

    def mostrar_info(self):

        return {
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "categoria": self.categoria.nombre,
            "valor_total": self.calcular_valor(),
            "descripcion": self.obtener_descripcion()
        }


# =========================
# HERENCIA: ELECTRONICO
# =========================

class Electronico(Producto):

    def __init__(
        self,
        nombre,
        precio,
        stock,
        categoria,
        garantia_meses
    ):

        super().__init__(
            nombre,
            precio,
            stock,
            categoria
        )

        self.garantia_meses = garantia_meses

    def obtener_descripcion(self):

        return (
            f"Electrónico: {self.nombre} | "
            f"Garantía: {self.garantia_meses} meses"
        )


# =========================
# HERENCIA: ALIMENTO
# =========================

class Alimento(Producto):

    def __init__(
        self,
        nombre,
        precio,
        stock,
        categoria,
        fecha_vencimiento
    ):

        super().__init__(
            nombre,
            precio,
            stock,
            categoria
        )

        self.fecha_vencimiento = fecha_vencimiento

    def obtener_descripcion(self):

        return (
            f"Alimento: {self.nombre} | "
            f"Vencimiento: {self.fecha_vencimiento}"
        )


# =========================
# HERENCIA: ROPA
# =========================

class Ropa(Producto):

    def __init__(
        self,
        nombre,
        precio,
        stock,
        categoria,
        talla
    ):

        super().__init__(
            nombre,
            precio,
            stock,
            categoria
        )

        self.talla = talla

    def obtener_descripcion(self):

        return (
            f"Ropa: {self.nombre} | "
            f"Talla: {self.talla}"
        )


# =========================
# CLASE MOVIMIENTO
# =========================

class Movimiento:

    def __init__(self, producto, tipo, cantidad):

        self.producto = producto
        self.tipo = tipo
        self.cantidad = cantidad
        self.fecha = datetime.now()

    def ejecutar(self):

        if self.tipo == "entrada":

            self.producto.aumentar_stock(
                self.cantidad
            )

            return True

        if self.tipo == "salida":

            return self.producto.disminuir_stock(
                self.cantidad
            )

        return False

    def mostrar_info(self):

        return {
            "producto": self.producto.nombre,
            "tipo": self.tipo,
            "cantidad": self.cantidad,
            "fecha": self.fecha.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }


# =========================
# CLASE INVENTARIO
# =========================

class Inventario:

    def __init__(self):

        self.productos = []
        self.movimientos = []

    def agregar_producto(self, producto):

        self.productos.append(producto)

    def eliminar_producto(self, nombre):

        for producto in self.productos:

            if producto.nombre == nombre:

                self.productos.remove(producto)

                return True

        return False

    def buscar_producto(self, nombre):

        for producto in self.productos:

            if producto.nombre.lower() == nombre.lower():

                return producto

        return None

    def registrar_movimiento(self, movimiento):

        if movimiento.ejecutar():

            self.movimientos.append(
                movimiento
            )

            return True

        return False

    def listar_productos(self):

        return [
            producto.mostrar_info()
            for producto in self.productos
        ]

    def valor_total_inventario(self):

        total = 0

        for producto in self.productos:

            total += producto.calcular_valor()

        return total