from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import MenuItem, Order
from .cart import Cart
import json

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

# 5. Checkout view - Kumaliza oda
def checkout_view(request):
    if request.method == 'POST':
        cart = Cart(request)
        
        jina = request.POST.get('jina')
        simu = request.POST.get('simu')
        email = request.POST.get('email', '')
        notes = request.POST.get('notes', '')
        
        # Kubanguza jumla
        jumla = cart.get_total_price()
        
        # Kurekodi items kwenye JSON
        items_data = []
        for item in cart:
            items_data.append({
                'name': item.get('chakula').name if item.get('chakula') else 'Unknown',
                'quantity': item['quantity'],
                'price': str(item['price']),
                'total': str(item['total_price'])
            })
        
        # Kuunda Order
        order = Order.objects.create(
            jina=jina,
            simu=simu,
            email=email,
            items_json=items_data,
            jumla=jumla,
            notes=notes
        )
        
        # Kutuma email kwa admin
        try:
            admin_message = f"""
Habari! Mteja mpya ameleta oda.

Taarifa za Mteja:
- Jina: {jina}
- Simu: {simu}
- Email: {email}

Vitu Vilivyoagizwa:
"""
            for item in items_data:
                admin_message += f"\n- {item['name']} x{item['quantity']} = {item['total']} TZS"
            
            admin_message += f"\n\nJumla ya Oda: {jumla} TZS\nKumbuka: {notes}"
            
            send_mail(
                subject=f"Oda Mpya: #{order.id} - {jina}",
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True
            )
        except Exception as e:
            print(f"Email error: {e}")
        
        # Kufuta kikapu baada ya oda
        cart.clear()
        
        return render(request, 'restaurant/order_success.html', {'order': order})
    
    return redirect('cart_detail')


# 6. Booking view - Kukamatia meza
def booking_view(request):
    if request.method == 'POST':
        from django.contrib import messages
        from .models import Reservation
        from datetime import datetime
        
        jina = request.POST.get('jina')
        simu = request.POST.get('simu')
        email = request.POST.get('email', '')
        idadi_ya_watu = request.POST.get('idadi_ya_watu')
        tarehe_na_muda = request.POST.get('tarehe_na_muda')
        ujumbe = request.POST.get('ujumbe')
        
        # Kuhifadhi kwenye Database
        reservation = Reservation.objects.create(
            jina=jina,
            simu=simu,
            idadi_ya_watu=idadi_ya_watu,
            tarehe_na_muda=tarehe_na_muda,
            ujumbe=ujumbe
        )
        
        # Kutuma email kwa admin
        try:
            admin_message = f"""
Habari! Mteja mpya amekamatia meza.

Taarifa za Mteja:
- Jina: {jina}
- Simu: {simu}
- Email: {email}
- Watu: {idadi_ya_watu}
- Tarehe na Muda: {tarehe_na_muda}
- Ujumbe: {ujumbe}
"""
            send_mail(
                subject=f"Booking Mpya: {jina}",
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True
            )
        except Exception as e:
            print(f"Email error: {e}")
        
        messages.success(request, f"Asante {jina}, meza yako imehifadhiwa kikamilifu!")
        return redirect('menu')
        
    return render(request, 'restaurant/booking.html')