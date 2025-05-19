let productos = [];

async function obtenerProductos() {
    const response = await fetch('/api/productos/');
    if (!response.ok) {
        return [];
    }
    return await response.json();
}

function mostrarResultados(resultados) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
    if (resultados.length === 0) {
        resultsDiv.innerHTML = '<p>No se encontraron productos.</p>';
        return;
    }
    resultados.forEach(producto => {
        const item = document.createElement('div');
        item.className = 'result-item';
        item.innerHTML = `
            <strong>ID:</strong> ${producto.id} - <strong>${producto.nombre}</strong> - $${producto.precio}
            ${producto.imagen ? `<br><img src="${producto.imagen}" alt="${producto.nombre}" style="max-width:150px;max-height:150px;">` : ''}
            <br><button onclick="agregarAlCarrito(${producto.id})">Agregar al carrito</button>
        `;
        resultsDiv.appendChild(item);
    });
}

function agregarAlCarrito(id) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const index = carrito.findIndex(item => item.id === id);
    if (index !== -1) {
        carrito[index].cantidad += 1;
    } else {
        carrito.push({ id: id, cantidad: 1 });
    }
    localStorage.setItem('carrito', JSON.stringify(carrito));
    mostrarCarrito();
}

function mostrarCarrito() {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    let carritoDiv = document.getElementById('carrito');
    if (!carritoDiv) {
        carritoDiv = document.createElement('div');
        carritoDiv.id = 'carrito';
        document.body.appendChild(carritoDiv);
    }
    if (carrito.length === 0) {
        carritoDiv.innerHTML = '<h2>Carrito vacío</h2>';
        return;
    }
    let total = 0;
    let html = '<h2>Carrito de compras</h2><ul>';
    carrito.forEach(item => {
        const producto = productos.find(p => p.id === item.id);
        if (producto) {
            const subtotal = producto.precio * item.cantidad;
            total += subtotal;
            html += `<li>
                ${producto.nombre} x ${item.cantidad} = $${subtotal}
                <button onclick="eliminarDelCarrito(${producto.id})">Eliminar</button>
            </li>`;
        }
    });
    html += `</ul><strong>Total: $${total}</strong><br>`;
    html += `<button onclick="pagarCarrito()">Pagar</button>`;
    carritoDiv.innerHTML = html;
}

function eliminarDelCarrito(id) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const index = carrito.findIndex(item => item.id === id);
    if (index !== -1) {
        if (carrito[index].cantidad > 1) {
            carrito[index].cantidad -= 1;
        } else {
            carrito.splice(index, 1); // Elimina el producto si la cantidad es 1
        }
    }
    localStorage.setItem('carrito', JSON.stringify(carrito));
    mostrarCarrito();
}

async function buscar() {
    const query = document.getElementById('search-bar').value.toLowerCase();
    const resultados = productos.filter(p =>
        p.nombre.toLowerCase().includes(query)
    );
    mostrarResultados(resultados);
}

function pagarCarrito() {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    let total = 0;
    carrito.forEach(item => {
        const producto = productos.find(p => p.id === item.id);
        if (producto) {
            total += producto.precio * item.cantidad;
        }
    });

    fetch('/pagar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ carrito: carrito, total: total })
    })
    .then(response => response.json())
    .then(data => {
        if (data.url) {
            window.location.href = data.url; // Redirige a Transbank
        } else {
            alert('Error al iniciar el pago');
        }
    });
}

// Función para obtener el CSRF token (si usas CSRF)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById('search-btn').addEventListener('click', buscar);
document.getElementById('search-bar').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') buscar();
});

// Al cargar la página, obtener productos de la API
obtenerProductos().then(data => {
    console.log("Productos recibidos:", data);
    productos = data;
    mostrarResultados(productos);
    mostrarCarrito();
});