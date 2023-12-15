from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import Registrar_usuario_email
from django.contrib.auth.models import User
from django.http import HttpResponse
from store.models import *


# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) 
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('store')
        else:
            messages.success(request, ("Usuario o contraseña incorrecto, intente nuevamente..."))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, ("Te haz deslogeado!"))
    return redirect('store')

def register_user(request):
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
                messages.add_message(request, messages.INFO, 'Passwords do not match')
                return redirect('register')
        else:
            return render(request, 'authenticate/register.html', {'form': form})
    else:
        form = Registrar_usuario_email()
        return render(request, 'authenticate/register.html', {"form":form})

