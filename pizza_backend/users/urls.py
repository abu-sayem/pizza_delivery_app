
from django.urls import include, path
from . import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [

    path('rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('sign_up/', include('dj_rest_auth.registration.urls')),
    #path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('', views.UserListView.as_view()),
]
