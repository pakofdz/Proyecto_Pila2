from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('new_rate/', views.create_rates, name='create_rates'),
    path('rates/', views.rates, name="rates"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
]