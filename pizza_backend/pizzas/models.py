from django.contrib.auth.models import AbstractUser
from django.db import models
#from django.contrib.gis.db import models
from django.core.validators import  MinValueValidator 
from enum import Enum
from datetime import datetime
from uuid import uuid4
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from users.models import User

#from filer.fields.image import FilerImageField


class Resturant(models.Model):
    name = models.CharField(_("Device Name"), max_length=100, blank=False, null=False, help_text="Device Name", default='')
    owner = models.ForeignKey(User, related_name='shops', on_delete=models.CASCADE)
    #image = FilerImageField(null=True, blank=True, related_name="resturant_image", on_delete=models.CASCADE, help_text="Upload/Select image for this resturant")
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    lat = models.FloatField(_("Latitude"), blank=True, default=0.0)
    lon = models.FloatField(_("Longitude"), blank=True, default=0.0)
    #loc = models.PointField(_("Location"), srid=4326, geography=True, dim=2, null=True, blank=True, editable=False)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Resturants"

    def __str__(self):
        return self.name



class Pizza(models.Model):
    class AVAILABLE(Enum):
        yes = ('yes', 'yes')
        no = ('no', 'no')
        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]
    name = models.CharField(max_length=250, unique=True)
    resturant = models.ForeignKey(Resturant, related_name='pizzas', on_delete=models.CASCADE)
    status = models.CharField(max_length=3,choices=[x.value for x in AVAILABLE], default='yes')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Order(models.Model):
    class STATUS(Enum):
        pending = ('pe', 'pending')
        delivered = ('de', 'delivered')
        in_progress = ('ip', 'in_progress' )
        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    class SIZES(Enum):
        small = ('sm', 'small')
        medium = ('md', 'medium')
        large = ('lg', 'large')
        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    size = models.CharField(max_length=2,choices=[x.value for x in SIZES], default='md')
    count = models.PositiveIntegerField(default=1,blank=False, validators=[MinValueValidator(1)])
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_as_customer_man')
    delivery_man = models.ForeignKey( User,null=True,blank=True,on_delete=models.DO_NOTHING,related_name='order_as_delivery_man')
    delivery_address = models.CharField(max_length=255)
    status = models.CharField(max_length=2,choices=[x.value for x in STATUS], default='pe')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pizza.name

    def order_detail(self):
        return reverse('pizza:pizza_detail', kwargs={'pizza_id': self.id})
