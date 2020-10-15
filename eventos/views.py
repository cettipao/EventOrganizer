from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def flyerView(request):
    return render(request, "home.html", {})

def invitadoView(request,inv):
    invitado = Invitado.objects.get(numero=inv)
    return render(request, "invitado.html", {"nombre":invitado.nombre, "numero": invitado.numero, "sexo":invitado.sexo})

def adminView(request):
    invitados = Invitado.objects.all()
    numHombres = len(Invitado.objects.filter(sexo="H"))
    numMujeres = len(Invitado.objects.filter(sexo="M"))
    return render(request, 'admin.html', {'invitados':invitados,'hombres':numHombres,'mujeres':numMujeres})