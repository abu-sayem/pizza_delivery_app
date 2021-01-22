from django.contrib import admin
from .models import Pizza, Order, Resturant

class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Pizza, PizzaAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('pizza','size', 'count', 'customer','delivery_address', 'status')
    list_filter = ('status',)
    readonly_fields = ('id', 'created_at', 'created_at',)
admin.site.register(Order, OrderAdmin)

class ResturantAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ('name', 'owner','photo', 'lon', 'lat',)
admin.site.register(Resturant, ResturantAdmin)
