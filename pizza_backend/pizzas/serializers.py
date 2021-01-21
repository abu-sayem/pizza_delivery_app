from rest_framework import serializers

from .models import Order, Pizza


from pizza_backend.users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username',]

class PizzaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pizza
        #fields = '__all__'
        exclude = ('created_at','updated_at' )


class OrderSerializerCreateRetrive(serializers.HyperlinkedModelSerializer):
    flavor = serializers.CharField(source='pizza.name')
    customer = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['flavor','size','count','customer', 'status']

class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        #fields = '__all__'
        exclude = ('created_at','updated_at' )
