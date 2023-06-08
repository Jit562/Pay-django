from django.contrib import admin

from .models import Cart, CartItem, Pizza, PizzaCat

# Register your models here.


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Pizza)
admin.site.register(PizzaCat)
