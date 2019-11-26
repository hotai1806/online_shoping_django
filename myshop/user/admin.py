from django.contrib import admin
from .models import Profile, Item, OrderItem, Order, Payment, Address, Wallet
# Register your models here.
from django.db.models import Sum

admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Wallet)
admin.site.register(Address)




class Money(admin.ModelAdmin):
    Companymoney = int(100)

    def get_money(self, request, queryset):
        totals = Payment.objects.all().aggregate(Sum('amount'))
        return totals
    pass
admin.site.register(Payment, Money)
