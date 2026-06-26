from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu_view, name='menu'),
    path('cart/add/<int:chakula_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:chakula_id>/', views.cart_remove, name='cart_remove'),
    path('cart/', views.cart_detail, name='cart_detail'),
    # Hapa chini utaongeza njia ya booking/reservation baadae mfano:
    # path('booking/', views.booking_view, name='booking'),
    path('booking/', views.booking_view, name='booking'),
]