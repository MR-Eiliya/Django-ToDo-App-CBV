from django.urls import path
from .views import auth_view, CustomLogoutView

app_name = 'accounts'

urlpatterns = [
    path('auth/', auth_view, name='auth'),   
    path('logout/', CustomLogoutView.as_view(), name='logout'), 
]