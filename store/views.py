from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.contrib import messages

# Create your views here.
def store(request):
    
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def rates(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    rates = Rates.objects.all()
    context = {'items':items, 'order':order, 'cartItems':cartItems, 'rates':rates}
    return render(request, 'store/rates.html', context)


def create_rates(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None  # O manejar usuarios anónimos de otra manera

    if 'imageRate' in request.FILES:
        image_rate = request.FILES['imageRate']
    else:
        image_rate = None

    rate = Rates(
        user=user,
        title=request.POST['title'],
        description=request.POST['description'],
        rate=request.POST['rate'],
        imageRate=image_rate
    )
    rate.save()
    return redirect('/rates/')


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action: ', action)
    print('productId: ', productId)

    user = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=user, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


#from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=True)
        name = user.first_name + " " + user.last_name
        email = user.email

    else:
        user, order = guestOrder(request, data)
        name = data['form']['name']
        email = data['form']['email']


    total = float(data['form']['total'])
    order.transaction_id =  transaction_id
    
    if total == float(order.get_cart_total):
        order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                user=user,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    
    # Recopilar detalles de los productos comprados
    items = order.orderitem_set.all()  # Asegúrate de tener una relación inversa configurada en el modelo OrderItem
    productos = '\n'.join([f'{item.product.name} (Cantidad: {item.quantity})' for item in items])

    domicilio = f"{data['shipping']['address']}, {data['shipping']['city']}, {data['shipping']['state']}\n{data['shipping']['zipcode']}"

    # Enviar correo electrónico después de procesar el pedido
    enviar_correo_compra(name, email, total, productos, domicilio)

    return JsonResponse('Payment complete!', safe=False)


def enviar_correo_compra(nombre, email, total, lista_productos, domicilio):
    asunto = 'Confirmación de compra'
    mensaje = f"""Hola {nombre},

    Gracias por tu compra de ${total}. 

    Detalles de la Orden:
    {lista_productos}

    Domicilio de entrega:
    {domicilio}

    Tu orden ha sido procesada exitosamente.
    """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(asunto, mensaje, email_from, recipient_list)