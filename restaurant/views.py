from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem
from .cart import Cart

# 1. View ya Kuonyesha Menu (Hii uliyokuwa nayo mwanzo, tumeiongezea tu kikapu)
def menu_view(request):
    items = MenuItem.objects.all()
    return render(request, 'restaurant/menu.html', {'items': items})

# 2. View ya Kuongeza Chakula Kwenye Kikapu
def cart_add(request, chakula_id):
    cart = Cart(request)
    chakula = get_object_or_404(MenuItem, id=chakula_id)
    cart.add(chakula=chakula)
    return redirect('cart_detail')

# 3. View ya Kufuta Chakula Kwenye Kikapu
def cart_remove(request, chakula_id):
    cart = Cart(request)
    chakula = get_object_or_404(MenuItem, id=chakula_id)
    cart.remove(chakula)
    return redirect('cart_detail')

# 4. View ya Ukurasa wa Kikapu (Cart Detail)
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'restaurant/cart_detail.html', {'cart': cart})
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Reservation
from datetime import datetime

def booking_view(request):
    if request.method == 'POST':
        jina = request.POST.get('jina')
        simu = request.POST.get('simu')
        idadi_ya_watu = request.POST.get('idadi_ya_watu')
        tarehe_na_muda = request.POST.get('tarehe_na_muda')
        ujumbe = request.POST.get('ujumbe')
        
        # Kuhifadhi kwenye Database
        Reservation.objects.create(
            jina=jina,
            simu=simu,
            idadi_ya_watu=idadi_ya_watu,
            tarehe_na_muda=tarehe_na_muda,
            ujumbe=ujumbe
        )
        
        messages.success(request, f"Asante {jina}, meza yako imehifadhiwa kikamilifu!")
        return redirect('menu') # Inamrudisha kwenye menu baada ya ku-book
        
    return render(request, 'restaurant/booking.html')