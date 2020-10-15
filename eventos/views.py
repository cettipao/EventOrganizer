from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def flyerView(request):
    return render(request, "home.html", {})

def invitadoView(request,inv):
    invitado = Invitado.objects.get(numero=inv)
    return render(request, "invitado.html", {"nombre":invitado.nombre, "numero": invitado.numero, "sexo":invitado.sexo})