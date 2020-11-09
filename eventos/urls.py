from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view()),
    path('sms/', smsView),
    path('invitado/<str:num>/<str:conf>/', invitadoView),
    path('invitado/<str:num>/', invitadoView),
    path('config/', configView),
    path('download/', downloadView),
]



