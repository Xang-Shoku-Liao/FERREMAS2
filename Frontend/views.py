from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from transbank.webpay.webpay_plus.transaction import Transaction
from django.shortcuts import render
from Productos.models import Producto
from .utils import obtener_valor_dolar
from datetime import datetime

@csrf_exempt
def pagar(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        carrito = data.get('carrito', [])
        total = data.get('total', 0)

        buy_order = "orden_" + str(request.user.id if request.user.is_authenticated else "anon") + "_" + str(total)
        session_id = "session_" + buy_order
        return_url = "http://127.0.0.1:8000/retorno/"

        # Guarda los datos en sesión
        request.session['carrito'] = carrito
        request.session['total'] = total

        response = Transaction().create(buy_order, session_id, total, return_url)
        return JsonResponse({'url': response['url'] + '?token_ws=' + response['token']})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def home(request):
    return render(request, 'frontend/index.html')

def retorno(request):
    token = request.GET.get('token_ws')
    carrito = request.session.get('carrito', [])
    total = request.session.get('total', 0)
    fecha = datetime.now()

    estado_pago = "desconocido"
    detalle = []
    respuesta_transbank = None
    razon_rechazo = ""

    if token:
        try:
            respuesta_transbank = Transaction().commit(token)
            if respuesta_transbank['status'] == 'AUTHORIZED':
                estado_pago = "aceptado"
            else:
                estado_pago = "rechazado"
                razon_rechazo = respuesta_transbank.get('response_code', 'Sin información')
        except Exception as e:
            estado_pago = "error"
            razon_rechazo = str(e)

    # Armar detalle de productos
    for item in carrito:
        try:
            producto = Producto.objects.get(id=item['id'])
            detalle.append({
                'nombre': producto.nombre,
                'marca': producto.marca,
                'cantidad': item['cantidad'],
            })
        except Producto.DoesNotExist:
            detalle.append({
                'nombre': 'Producto no encontrado',
                'marca': '',
                'cantidad': item['cantidad'],
            })

    return render(request, 'frontend/retorno.html', {
        'carrito': detalle,
        'total': total,
        'fecha': fecha,
        'estado_pago': estado_pago,
        'razon_rechazo': razon_rechazo,
    })

def lista_productos(request):
    productos = Producto.objects.all()
    valor_dolar = obtener_valor_dolar()
    productos_con_dolar = []
    for producto in productos:
        precio_usd = round(producto.precio / valor_dolar, 2) if valor_dolar else 0
        productos_con_dolar.append({
            'nombre': producto.nombre,
            'marca': producto.marca,
            'precio_clp': producto.precio,
            'precio_usd': precio_usd,
        })
    return render(request, 'frontend/index.html', {
        'productos': productos_con_dolar,
        'valor_dolar': valor_dolar,
    })

def api_productos(request):
    productos = Producto.objects.all()
    valor_dolar = obtener_valor_dolar()
    productos_json = []
    for producto in productos:
        precio_usd = round(producto.precio / valor_dolar, 2) if valor_dolar else 0
        productos_json.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'marca': producto.marca,
            'precio': producto.precio,
            'precio_usd': precio_usd,  # <-- asegúrate de incluir este campo
            'imagen': producto.imagen.url if producto.imagen else None,
        })
    return JsonResponse(productos_json, safe=False)