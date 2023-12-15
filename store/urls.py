from django.urls import path
from . import views
from .views import list_rates,create_rates

urlpatterns = [
    
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('rates/', views.rates, name="rates"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    path('list/', list_rates, name='list_rates'),
    path('new/', create_rates, name='create_rates')
]