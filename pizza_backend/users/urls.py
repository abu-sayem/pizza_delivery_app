
from django.urls import include, path
from django.contrib import admin
from . import views
from rest_framework_simplejwt import views as jwt_views

from allauth.account.views import ConfirmEmailView

'''
/auth/login/ (POST)
/auth/logout/ (POST)
/auth/password/reset/ (POST)
/auth/password/reset/confirm/ (POST)
/auth/password/change/ (POST)
/auth/user/ (GET, PUT, PATCH)
/auth/token/verify/ (POST)
/auth/token/refresh/ (POST)
/auth/registration/ (POST)
/auth/registration/verify-email/ (POST)
/auth/facebook/ (POST)
/auth/twitter/ (POST
'''

urlpatterns = [
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('sign_up/confirm-email/<str:key>/', ConfirmEmailView.as_view(),name='account_confirm_email'),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('admin/', admin.site.urls),
    path('sign_up/', include('dj_rest_auth.registration.urls')),
    path('', include('dj_rest_auth.urls')),
    #path('', views.UserListView.as_view()),
]
