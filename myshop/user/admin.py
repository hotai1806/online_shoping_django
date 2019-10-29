from django.contrib import admin
from .models import Profile, Item, OrderItem, Order, Payment, Address
# Register your models here.

admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Address)
