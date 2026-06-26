from django.db import models

# 1. Model ya Meza za Mgahawa (Sahihisha iwe class)
class RestaurantTable(models.Model):
    table_number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField(default=4)
    is_available = models.BooleanField(default=True)

    def _str_(self):
        return f"Meza Namba {self.table_number}"


# 2. Model ya Menyu (Vyakula na Vinywaji - Sahihisha iwe class)
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('chakula', 'Chakula'),
        ('kinywaji', 'Kinywaji'),
        ('kitoweo', 'Kitoweo/Vitafunio'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='chakula')
    
    # ONGEZA HUU MSTARI HAPA CHINI KWA AJILI YA PICHA (Hatua ya 3)
    image = models.ImageField(upload_to='vyakula/', blank=True, null=True)

    def _str_(self):
        return self.name


# 3. Model Mpya ya Booking/Reservation (Hatua ya 2)
class Reservation(models.Model):
    jina = models.CharField(max_length=100)
    simu = models.CharField(max_length=15)
    idadi_ya_watu = models.IntegerField()
    tarehe_na_muda = models.DateTimeField()
    ujumbe = models.TextField(blank=True, null=True)
    tarehe_ya_kuomba = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.jina} - Watu {self.idadi_ya_watu}"
    is_available = models.BooleanField(default=True)