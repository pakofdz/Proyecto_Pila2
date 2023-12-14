from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,("Registration successful!"))

            user_model = User.objects.get(username=name)
            new_customer = Customer.objects.create(user=user_model, name=name, email=email)
            new_customer.save()

            return redirect('store')
    else:
        form = UserCreationForm()
    return render(request, 'authenticate/register.html', {
        'form':form,
        })