from django.contrib import admin
from .models import MenuItem, RestaurantTable, Reservation, Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'jina', 'simu', 'jumla', 'status', 'tarehe_ya_kuagiza')
    list_filter = ('status', 'tarehe_ya_kuagiza')
    search_fields = ('jina', 'simu', 'email')
    readonly_fields = ('tarehe_ya_kuagiza', 'items_json')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('jina', 'simu', 'idadi_ya_watu', 'tarehe_na_muda', 'tarehe_ya_kuomba')
    list_filter = ('tarehe_na_muda', 'tarehe_ya_kuomba')
    search_fields = ('jina', 'simu')

# Register your models here.
admin.site.register(RestaurantTable)
admin.site.register(MenuItem)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Order, OrderAdmin)