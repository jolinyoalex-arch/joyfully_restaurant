from django.contrib import admin
from .models import MenuItem, RestaurantTable, Reservation

# Register your models here.
admin.site.register(RestaurantTable)
admin.site.register(MenuItem)
admin.site.register(Reservation)