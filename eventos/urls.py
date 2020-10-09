from django.urls import path
from .views import flyerView

urlpatterns = [
    path('',flyerView),
]