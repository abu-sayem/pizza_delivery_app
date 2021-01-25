from pizzas.models import Order
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from .serializers import NestedOrderSerializer, OrderSerializer, OrderSerializerv2

# class PizzaConsumer(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         user = self.scope['user']
#         if user.is_anonymous:
#             await self.close()
#         else:
#             user_group = await self._get_user_group(user)
#             if user_group == 'delivery_man':
#                 await self.channel_layer.group_add(
#                     group='delivery_man',
#                     channel=self.channel_name
#                 )
#             for order_id in await self._get_order_ids(user):
#                 await self.channel_layer.group_add(
#                     group=order_id,
#                     channel=self.channel_name
#                 )

#             await self.accept()

#     async def receive_json(self, content, **kwargs):
#         message_type = content.get('type')
#         if message_type == 'create.order':
#             await self.create_order(content)
#         elif message_type == 'echo.message':
#             await self.echo_message(content)

#     async def create_order(self, message):
#         data = message.get('data')
#         order = await self._create_order(data)
#         order_data = NestedOrderSerializer(order).data
#         await self.channel_layer.group_send(group='drivers', message={
#             'type': 'echo.message',
#             'data': order_data
#         })

#         await self.channel_layer.group_add( 
#         group=f'{order.id}',
#         channel=self.channel_name
#     )

#         await self.send_json({
#         'type': 'echo.message',
#         'data': order_data,
#     })

#     async def echo_message(self, message):
#         await self.send_json(message)

#     async def disconnect(self, code):
#         user = self.scope['user']
#         user_group = await self._get_user_group(user)
#         if user_group == 'delivery_man':
#             await self.channel_layer.group_discard(
#                 group='delivery_man',
#                 channel=self.channel_name
#             )
#         for trip_id in await self._get_trip_ids(user):
#             await self.channel_layer.group_discard(
#                 group=trip_id,
#                 channel=self.channel_name
#             )
#         await super().disconnect(code)


#     @database_sync_to_async
#     def _create_order(self, data):
#         serializer = OrderSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         return serializer.create(serializer.validated_data)

#     @database_sync_to_async
#     def _get_user_group(self, user):
#         return user.groups.first().name

#     @database_sync_to_async
#     def _get_order_ids(self, user):
#         user_groups = user.groups.values_list('name', flat=True)
#         if 'delivery_man' in user_groups:
#             trip_ids = user.order_as_delivery_man.exclude(
#                 status=Order.pending
#             ).only('id').values_list('id', flat=True)
#         else:
#             trip_ids = user.order_as_customer_man.exclude(
#                 status=Order.delivered
#             ).only('id').values_list('id', flat=True)
#         return map(str, trip_ids)







class PizzaConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if user.is_anonymous:
            await self.close()
        else:
            user_group = await self._get_user_group(user) # new
            if user_group == 'delivery_man':
                await self.channel_layer.group_add(
                    group='delivery_man',
                    channel=self.channel_name
                )
            for order_id in await self._get_order_ids(user):
                await self.channel_layer.group_add(
                    group=order_id,
                    channel=self.channel_name
                )
            await self.accept()

    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        if message_type == 'create.order':
            await self.create_order(content)
        elif message_type == 'echo.message':
            await self.echo_message(content)
        elif message_type == 'update.order':
            await self.update_order(content)

    async def echo_message(self, message):
        await self.send_json({
            'type': message.get('type'),
            'data': message.get('data'),
        })

    async def disconnect(self, code):
        user = self.scope['user'] # new
        user_group = await self._get_user_group(user)
        if user_group == 'customer':
            await self.channel_layer.group_discard(
                group='customer',
                channel=self.channel_name
            )
        for order_id in await self._get_order_ids(user):
            await self.channel_layer.group_discard(
                group=order_id,
                channel=self.channel_name
            )

        await super().disconnect(code)

    @database_sync_to_async
    def _get_user_group(self, user):
        return user.groups.first().name

    async def create_order(self, message):
        data = message.get('data')
        order = await self._create_order(data)
        order_data = NestedOrderSerializer(order).data
        # Send rider requests to all drivers.
        await self.channel_layer.group_send(group='delivery_man', message={
            'type': 'echo.message',
            'data': order_data
        })

        # Add rider to trip group.
        await self.channel_layer.group_add( # new
            group=f'{order.id}',
            channel=self.channel_name
        )

        await self.send_json({
            'type': 'echo.message',
            'data': order_data,
        })

    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        if message_type == 'create.order':
            await self.create_order(content)
        elif message_type == 'echo.message':
            await self.echo_message(content)
        elif message_type == 'update.order': 
            await self.update_order(content)


    async def update_order(self, message):
        data = message.get('data')
        order = await self._update_order(data)
        order_id = f'{order.id}'
        order_data = NestedOrderSerializer(order).data

        # Send update to rider.
        await self.channel_layer.group_send(
            group=order_id,
            message={
                'type': 'echo.message',
                'data': order_data,
            }
        )

        # Add driver to the trip group.
        await self.channel_layer.group_add(
            group=order_id,
            channel=self.channel_name
        )

        await self.send_json({
            'type': 'echo.message',
            'data': order_data
        })

    

    async def echo_message(self, message):
        await self.send_json(message)

    @database_sync_to_async
    def _create_order(self, data):
        serializer = OrderSerializerv2(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.create(serializer.validated_data)

    @database_sync_to_async
    def _update_order(self, data):
        instance = Order.objects.get(id=data.get('id'))
        serializer = OrderSerializerv2(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.update(instance, serializer.validated_data)

    @database_sync_to_async
    def _get_order_ids(self, user):
        user_groups = user.groups.values_list('name', flat=True)
        if 'delivery_man' in user_groups:
            order_ids = user.order_as_delivery_man.exclude(
                status='delivered'
            ).only('id').values_list('id', flat=True)
        else:
            order_ids = user.order_as_customer_man.exclude(
                status='delivered'
            ).only('id').values_list('id', flat=True)
        return map(str, order_ids)
