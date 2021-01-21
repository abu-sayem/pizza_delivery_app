from django.contrib import admin
from .models import Pizza, Order

class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Pizza, PizzaAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('pizza','size', 'count', 'customer','status')
admin.site.register(Order, OrderAdmin)
