from django.urls import path
from django.contrib.auth.views import LogoutView

from user_authentication.views import user_login, user_create, UpdateProfile, user_password_change

app_name = 'user_authentication'

urlpatterns = [
    path('registration/', user_create, name='signin'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='log_out'),
    path('detail/', UpdateProfile.as_view(), name='profile'),
    path('change_password/', user_password_change, name='change_password'),
]
