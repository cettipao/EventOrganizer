from django.urls import path
from .views import *

urlpatterns = [
    path('', flyerView),
    path('invitado/<str:inv>', invitadoView),
    path('sms/', smsView),
]