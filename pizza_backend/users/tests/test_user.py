# from django.contrib.auth import get_user_model
# from rest_framework import status
# from rest_framework.reverse import reverse
# from rest_framework.test import APITestCase

# PASSWORD = 'pAssw0rd!'


# class AuthenticationTest(APITestCase):
#     def test_user_can_sign_up(self):
#         response = self.client.post(reverse('rest_register'), data={
#             'username': 'user@example.com',
#             'email': 'user@example.com',
#             'password1': PASSWORD,
#             'password2': PASSWORD,
#         })
#         user = get_user_model().objects.last()
#         self.assertEqual(status.HTTP_201_CREATED, response.status_code)
#         self.assertEqual(response.data['user']['pk'], str(user.pk))
#         self.assertEqual(response.data['user']['email'], user.email)
