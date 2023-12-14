from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('rates/', views.rates, name="rates"),
    path('login/', views.login_usuario, name="login"),
    path('register/', views.registrar_usuario, name="register"),
    path('logout/', views.logout_usuario, name='logout'),
    

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
]