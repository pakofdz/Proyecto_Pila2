from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder


from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from .forms import Registrar_usuario_email 

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

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/rates.html', context)


def login_usuario(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST.get("pasword")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            return redirect('login')
    else:
        return redirect('login') 

def logout_usuario(request):
    logout(request)
    return redirect('login')

def registrar_usuario(request):
    if request.method == "POST":
        form = Registrar_usuario_email(request.POST)
        if form.is_valid():
            name = request.POST['username']
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password1']
            password2 = request.POST['password2']

            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email alredy exists')
                    return redirect('register')
                elif User.objects.filter(username=name).exists():
                    messages.info(request, 'This username is alredy taken')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=name, first_name=firstname, last_name=lastname, email=email, password=password)
                    user.save()

                    user_model = User.objects.get(username=name)
                    new_customer = Customer.objects.create(user=user_model, name=name, email=email)
                    new_customer.save()

                    user_auth = authenticate(username=name, password=password)
                    login(request, user_auth)
                    return redirect('store')
            else:
                messages.info(request, 'Passwords do not match') 
                return redirect('register')      

            
    else:
        form = Registrar_usuario_email()
        return render(request, 'store/user_register.html', {"form":form})


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action: ', action)
    print('productId: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

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
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        name = customer.name
        email = customer.email

    else:
        customer, order = guestOrder(request, data)
        name = data['form']['name']
        email = data['form']['email']


    total = float(data['form']['total'])
    order.transaction_id =  transaction_id
    
    if total == float(order.get_cart_total):
        order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
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