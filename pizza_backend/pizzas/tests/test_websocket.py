
from os import wait
import pytest
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import AccessToken
from pizzas.models import Pizza, Resturant

from pizza_backend.routing import application
from pizzas.models import Order


TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}



# @database_sync_to_async
# def create_user(email,password,group='rider'):
#     user = get_user_model().objects.create_user(email=email,password=password)

#     # Create user group.
#     user_group, _ = Group.objects.get_or_create(name=group)
#     user.groups.add(user_group)
#     user.save()

#     # Create access token.
#     access = AccessToken.for_user(user)
#     return user, access


# @pytest.mark.asyncio
# class TestWebSocket:
#     async def test_can_connect_to_server(self, settings):
#         settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
#         communicator = WebsocketCommunicator(
#             application=application,
#             path='/pizza/'
#         )
#         connected, _ = await communicator.connect()
#         print(connected)
#         #assert connected is True
#         await communicator.disconnect()

 



@database_sync_to_async
def create_user(email,password,group='customer'):
    user = get_user_model().objects.create_user(email=email,password=password)

    # Create user group.
    user_group, _ = Group.objects.get_or_create(name=group) # new
    user.groups.add(user_group)
    user.save()

    # Create access token.
    access = AccessToken.for_user(user)
    return user, access



owner = create_user("owner@owner.com", "passowRD")
customer = create_user("customer@customer.com", "passowRD", "customer")
delivery_man = create_user("deli_man@deli_man.com", "passowRD", "customer")

@database_sync_to_async
def create_resturant():
    resturant = Resturant(name="sample Resturant", owner=owner)
    resturant.save()
    return resturant


@database_sync_to_async
def create_pizza(name, owner):
    resturant = Resturant(name="sample Resturant1", owner=owner)
    resturant.save()
    pizza = Pizza.objects.create(name=name, resturant=resturant)
    pizza.save()
    return pizza
    

@database_sync_to_async
def create_order(pizza,customer,delivery_man,delivery_address):
    order =  Order(
        pizza=pizza,
        customer=customer,
        delivery_man=delivery_man,
        delivery_address=delivery_address,
    )
    order.save()
    return order




@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestWebSocket:
    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(  # new
            'test.user@example.com', 'pAssw0rd'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/pizza/?token={access}' # changed
        )
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()



    async def test_can_send_and_receive_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'test.user@example.com', 'pAssw0rd'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/pizza/?token={access}'
        )
        connected, _ = await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()


    # async def test_can_send_and_receive_broadcast_messages(self, settings):
    #     settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    #     communicator = WebsocketCommunicator(
    #         application=application,
    #         path='/pizza/'
    #     )
    #     connected, _ = await communicator.connect()
    #     message = {
    #         'type': 'echo.message',
    #         'data': 'This is a test message.',
    #     }
    #     channel_layer = get_channel_layer()
    #     await channel_layer.group_send('test', message=message)
    #     response = await communicator.receive_json_from()
    #     assert response == message
    #     await communicator.disconnect()

    # async def test_cannot_connect_to_socket(self, settings):
    #     settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    #     communicator = WebsocketCommunicator(
    #         application=application,
    #         path='/pizza/'
    #     )
    #     connected, _ = await communicator.connect()
    #     assert connected is False



#----------------------------------------------------------
    async def test_join_driver_pool(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'test.user@example.com', 'pAssw0rd', 'delivery_man'
        )
        # owner, _ = await create_user("owner@owner.com", "passowRD")
        # customer, _ = await create_user("customer@customer.com", "passowRD", "customer")
        # delivery_man, _ = await create_user("deli_man@deli_man.com", "passowRD", "customer")
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/pizza/?token={access}'
        )
        connected, _ = await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send('delivery_man', message=message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()


    async def test_request_order(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, _ = await create_user(
            'test.usesder@example.com', 'pAssw0rd', 'customer'
        )
        owner, _ = await create_user("owneesdr@owner.com", "passowRD")
        customer, access = await create_user("cuddsteomer@customer.com", "passowRD", "customer")
        delivery_man, _ = await create_user("deli_meandd@deli_man.com", "passowRD", "delivery_man")
        pizza = await create_pizza("merinesdsata", owner)
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/pizza/?token={access}'
        )
        connected, _ = await communicator.connect()
        await communicator.send_json_to({
            'type': 'create.order',
            'data': {
                'pizza': pizza.id,
                'customer': str(customer.id),
                'delivery_man': str(delivery_man.id),
                'delivery_address': "Sutraput Police Station"
            },
        })
        response = await communicator.receive_json_from()
        response_data = response.get('data')
        assert response_data['id'] is not None
        assert response_data['delivery_address'] == "Sutraput Police Station"
        await communicator.disconnect()






    async def test_delivery_man_alerted_on_request(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS

        # Listen to the 'drivers' group test channel.
        channel_layer = get_channel_layer()
        await channel_layer.group_add(
            group='delivery_man',
            channel='test_channel'
        )

        user, _ = await create_user(
            'test.usehgjhgr@example.com', 'pAssw0rd', 'customer'
        )
        owner, _ = await create_user("ownehjhgr@owners.com", "passowRD")
        customer, access = await create_user("custghjghomer@customers.com", "passowRD","customer")
        delivery_man, _ = await create_user("deli_makjlkn@deli_mans.com", "passowRD","delivery_man")
        pizza = await create_pizza("Mazrgarita", owner)
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/pizza/?token={access}'
        )
        connected, _ = await communicator.connect()

        # Request a trip.
        await communicator.send_json_to({
            'type': 'create.order',
            'data': {
                'pizza': pizza.id,
                'customer': str(customer.id),
                'delivery_man': str(delivery_man.id),
                'delivery_address': "Sutraput Police Station"
            },
        })

        # Receive JSON message from server on test channel.
        response = await channel_layer.receive('test_channel')
        response_data = response.get('data')

        assert response_data['id'] is not None
        assert response_data['delivery_man']['email'] is not None
        #print(response_data)
        await communicator.disconnect()







    async def test_create_trip_group(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, _ = await create_user(
            'test.usehgjhgr@example.com', 'pAssw0rd', 'customer'
        )
        owner, _ = await create_user("ownehjhgr@owners.com", "passowRD")
        customer, access = await create_user("custghjghomer@customers.com", "passowRD","customer")
        delivery_man, _ = await create_user("deli_makjlkn@deli_mans.com", "passowRD","delivery_man")
        pizza = await create_pizza("Mazrgarita", owner)
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/pizza/?token={access}'
        )
        connected, _ = await communicator.connect()

        # Send a ride request.
        await communicator.send_json_to({
            'type': 'create.order',
            'data': {
                'pizza': pizza.id,
                'customer': str(customer.id),
                'delivery_man': str(delivery_man.id),
                'delivery_address': "Sutraput Police Station"
            },
        })
        response = await communicator.receive_json_from()
        response_data = response.get('data')

        # Send a message to the trip group.
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send(response_data['id'], message=message)

        # Rider receives message.
        response = await communicator.receive_json_from()
        assert response == message

        await communicator.disconnect()









    async def test_join_order_group_on_connect(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, _ = await create_user(
            'test.usehgjhssagr@example.com', 'pAssw0rd', 'customer'
        )
        owner, _ = await create_user("ownehjashgr@owners.com", "passowRD")
        customer, access = await create_user("custghasjghomer@customers.com", "passowRD","customer")
        delivery_man, _ = await create_user("deli_makasjlkn@deli_mans.com", "passowRD","delivery_man")
        pizza = await create_pizza("Mazasrgarita", owner)
        order = await create_order(pizza,customer,delivery_man,"savar")
        #print(dir(order))
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/pizza/?token={access}'
        )
        connected, _ = await communicator.connect()

        # Send a message to the trip group.
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send(f'{order.id}', message=message)

        # Rider receives message.
        response = await communicator.receive_json_from()
        assert response == message

        await communicator.disconnect()





    async def test_delivery_man_can_update_order(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS

        # Create trip request.
        user, _ = await create_user(
            'test.usehgjhssagr@example.com', 'pAssw0rd', 'customer'
        )
        owner, _ = await create_user("ownehjashgr@owners.com", "passowRD", 'customer')
        customer, _ = await create_user("custghasjghomer@customers.com", "passowRD","customer")
        delivery_man, access = await create_user("deli_makasjlkn@deli_mans.com", "passowRD","delivery_man")
        pizza = await create_pizza("Mazasrgarita", owner)
        order = await create_order(pizza,customer,delivery_man,"savar")
        order_id = f'{order.id}'

        # Listen for messages as rider.
        channel_layer = get_channel_layer()
        await channel_layer.group_add(
            group=order_id,
            channel='test_channel'
        )

        # Update trip.
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/pizza/?token={access}'
        )
        connected, _ = await communicator.connect()
        # message = {
        #     'type': 'update.order',
        #     'data': {
        #         'id': order_id,
        #         'pizza': pizza.id,
        #         'status': 'in_progress',
        #         'customer': str(customer.id),
        #         'delivery_man': str(delivery_man.id),
        #         'delivery_address': "Sutraput Police Station"
        #     },
        # }



        await communicator.send_json_to({
            'type': 'update.order',
            'data': {
                'id': order_id,
                'pizza': pizza.id,
                'customer': str(customer.id),
                'delivery_man': str(delivery_man.id),
                'size': 'lg',
                'delivery_address': "Sutraput Police Station"
            },
        })



        #await communicator.send_json_to(message)

        # Rider receives message.
        response = await channel_layer.receive('test_channel')
        response_data = response.get('data')
        assert response_data['id'] == order_id
        print(response_data)
        await communicator.disconnect()




    async def test_driver_join_trip_group_on_connect(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        owner, _ = await create_user("ownehjashgr@owners.com", "passowRD", 'customer')
        customer, _ = await create_user("custghasjghomer@customers.com", "passowRD","customer")
        delivery_man, access = await create_user("deli_makasjlkn@deli_mans.com", "passowRD","delivery_man")
        pizza = await create_pizza("Mazasrgarita", owner)
        order = await create_order(pizza,customer,delivery_man,"savar")
        order_id = f'{order.id}'
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/pizza/?token={access}'
        )
        connected, _ = await communicator.connect()

        # Send a message to the trip group.
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send(f'{order.id}', message=message)

        # Rider receives message.
        response = await communicator.receive_json_from()
        assert response == message

        await communicator.disconnect()
