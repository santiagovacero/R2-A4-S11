const API = "";

let todosLosProductos = [];


// ==========================================
// CARGAR PRODUCTOS
// ==========================================

async function cargarProductos() {

    const respuesta = await fetch(
        `${API}/api/productos`
    );

    todosLosProductos =
        await respuesta.json();

    mostrarProductos(
        todosLosProductos
    );
}


// ==========================================
// MOSTRAR PRODUCTOS
// ==========================================

function mostrarProductos(productos) {

    const contenedor =
        document.getElementById(
            "productos"
        );

    contenedor.innerHTML = "";


    if (productos.length === 0) {

        contenedor.innerHTML =
            "<p>No se encontraron repuestos.</p>";

        return;
    }


    productos.forEach(producto => {

        const div =
            document.createElement("div");

        div.className = "producto";


        div.innerHTML = `
            <h3>${producto.nombre}</h3>

            <p>
                Precio: $${producto.precio}
            </p>

            <p>
                Stock: ${producto.stock}
            </p>

            <p>
                Categoría: ${producto.categoria}
            </p>

            <p>
                Valor total: $${producto.valor_total}
            </p>

            <p>
                ${producto.descripcion}
            </p>

            <button
                onclick="editarProducto(
                    '${producto.nombre}',
                    ${producto.precio},
                    ${producto.stock},
                    '${producto.categoria}'
                )"
            >
                Editar
            </button>

            <button
                onclick="eliminarProducto('${producto.nombre}')"
            >
                Eliminar
            </button>
        `;


        contenedor.appendChild(div);

    });
}


// ==========================================
// FILTRAR PRODUCTOS
// ==========================================

function filtrarProductos() {

    const texto =
        document.getElementById(
            "busqueda"
        ).value.toLowerCase();


    const categoria =
        document.getElementById(
            "filtroCategoria"
        ).value;


    const productosFiltrados =
        todosLosProductos.filter(
            producto => {

                const coincideNombre =
                    producto.nombre
                        .toLowerCase()
                        .includes(texto);


                const coincideCategoria =
                    categoria === "todas" ||
                    producto.categoria === categoria;


                return (
                    coincideNombre &&
                    coincideCategoria
                );

            }
        );


    mostrarProductos(
        productosFiltrados
    );
}


// ==========================================
// LIMPIAR FILTROS
// ==========================================

function limpiarFiltros() {

    document.getElementById(
        "busqueda"
    ).value = "";


    document.getElementById(
        "filtroCategoria"
    ).value = "todas";


    mostrarProductos(
        todosLosProductos
    );
}




async function agregarProducto() {

    const nombre =
        document.getElementById(
            "nombre"
        ).value;


    const precio =
        document.getElementById(
            "precio"
        ).value;


    const stock =
        document.getElementById(
            "stock"
        ).value;


    const tipo =
        document.getElementById(
            "tipo"
        ).value;


    if (
        nombre === "" ||
        precio === "" ||
        stock === ""
    ) {

        alert(
            "Completa todos los campos"
        );

        return;
    }


    const respuesta = await fetch(
        `${API}/api/productos`,
        {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({

                nombre: nombre,

                precio: precio,

                stock: stock,

                tipo: tipo

            })
        }
    );


    const resultado =
        await respuesta.json();


    alert(
        resultado.mensaje ||
        resultado.error
    );


    document.getElementById(
        "nombre"
    ).value = "";


    document.getElementById(
        "precio"
    ).value = "";


    document.getElementById(
        "stock"
    ).value = "";


    await cargarProductos();
}


// ==========================================
// ELIMINAR PRODUCTO
// ==========================================

async function eliminarProducto(nombre) {

    const confirmar =
        confirm(
            `¿Deseas eliminar "${nombre}"?`
        );


    if (!confirmar) {

        return;
    }


    const respuesta = await fetch(

        `${API}/api/productos/${encodeURIComponent(nombre)}`,

        {
            method: "DELETE"
        }

    );


    const resultado =
        await respuesta.json();


    alert(
        resultado.mensaje ||
        resultado.error
    );


    await cargarProductos();
}


// ==========================================
// EDITAR PRODUCTO
// ==========================================

async function editarProducto(
    nombreActual,
    precioActual,
    stockActual,
    categoriaActual
) {

    const nuevoNombre =
        prompt(
            "Nombre del repuesto:",
            nombreActual
        );


    if (nuevoNombre === null) {
        return;
    }


    const nuevoPrecio =
        prompt(
            "Precio:",
            precioActual
        );


    if (nuevoPrecio === null) {
        return;
    }


    const nuevoStock =
        prompt(
            "Stock:",
            stockActual
        );


    if (nuevoStock === null) {
        return;
    }


    let nuevoTipo;


    if (categoriaActual === "Frenos") {

        nuevoTipo = "frenos";

    } else if (
        categoriaActual === "Motor"
    ) {

        nuevoTipo = "motor";

    } else if (
        categoriaActual === "Transmisión"
    ) {

        nuevoTipo = "transmision";

    } else {

        nuevoTipo = "otros";
    }


    const respuesta = await fetch(

        `${API}/api/productos/${encodeURIComponent(nombreActual)}`,

        {

            method: "PUT",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({

                nombre: nuevoNombre,

                precio: nuevoPrecio,

                stock: nuevoStock,

                tipo: nuevoTipo

            })

        }

    );


    const resultado =
        await respuesta.json();


    alert(
        resultado.mensaje ||
        resultado.error
    );


    await cargarProductos();
}


// ==========================================
// REGISTRAR MOVIMIENTO
// ==========================================

async function registrarMovimiento() {

    const producto =
        document.getElementById(
            "productoMovimiento"
        ).value.trim();


    const tipo =
        document.getElementById(
            "tipoMovimiento"
        ).value;


    const cantidad =
        document.getElementById(
            "cantidadMovimiento"
        ).value;


    if (
        producto === "" ||
        cantidad === ""
    ) {

        alert(
            "Completa todos los campos"
        );

        return;
    }


    if (Number(cantidad) <= 0) {

        alert(
            "La cantidad debe ser mayor que 0"
        );

        return;
    }


    const respuesta = await fetch(
        `${API}/api/movimientos`,
        {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({

                producto: producto,

                tipo: tipo,

                cantidad: Number(cantidad)

            })

        }
    );


    const resultado =
        await respuesta.json();


    alert(
        resultado.mensaje ||
        resultado.error
    );


    if (respuesta.ok) {

        document.getElementById(
            "productoMovimiento"
        ).value = "";


        document.getElementById(
            "cantidadMovimiento"
        ).value = "";


        await cargarProductos();

        await cargarMovimientos();

    }

}


// ==========================================
// CARGAR HISTORIAL
// ==========================================

async function cargarMovimientos() {

    const respuesta = await fetch(
        `${API}/api/movimientos`
    );


    const movimientos =
        await respuesta.json();


    const contenedor =
        document.getElementById(
            "movimientos"
        );


    contenedor.innerHTML = "";


    movimientos.forEach(movimiento => {

        const div =
            document.createElement("div");


        div.className = "producto";


        div.innerHTML = `

            <h3>
                ${movimiento.producto}
            </h3>

            <p>
                Tipo: ${movimiento.tipo}
            </p>

            <p>
                Cantidad: ${movimiento.cantidad}
            </p>

            <p>
                Fecha: ${movimiento.fecha}
            </p>

        `;


        contenedor.appendChild(div);

    });
}


// ==========================================
// INICIAR
// ==========================================

cargarProductos();

cargarMovimientos();