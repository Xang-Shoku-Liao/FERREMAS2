from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from transbank.webpay.webpay_plus.transaction import Transaction
from django.shortcuts import render
from Productos.models import Producto
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

    detalle = []
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
    })