from django.contrib import admin
from .models import Profile, Item, OrderItem, Order, Payment, Address
# Register your models here.
from django.db.models import Sum

admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Address)



Companymoney = int(100)
# class Money(admin.ModelAdmin):
#
#     a = Payment.objects.values('amount').annotate(aa = Sum("amount"))
#     Companymoney += a
#     pass
#
# admin.site.register(Money)
