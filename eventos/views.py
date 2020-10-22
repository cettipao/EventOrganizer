import os

from django.shortcuts import render
from config.settings import BASE_DIR
from django_twilio.decorators import twilio_view
from twilio.twiml.messaging_response import MessagingResponse,Message
from .models import Invitado
from .imageGenerator import genImage, deleteImgs
from .excelGenerator import genExcel
import json
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404


# Create your views here.
"""
flyerView
Renderiza la pagina promocion del evento, sin ninguna logica

No toma parametros adicionales por url
"""
def flyerView(request):
    return render(request, "home.html", {})

"""
downloadView
Busca todos los invitados y mediante genExcel devuelve un .xlsx con los mismos

No toma parametros adicionales por url
"""
def downloadView(request):
    invitados = Invitado.objects.all() #Busca invitados
    genExcel(invitados) #Genera el Excel
    file_path = BASE_DIR + '/static/' + 'InvitadosEvento.xlsx' #Busca el excel generado
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404 #Devuelve el excel

"""
InvitadoView
- Muestra una tarjeta virtual del invitado.
- En modo superusuario al acceder, automaticamente el invitado pasa a estar adentro del evento
    (Patovica con cuenta superuser escanea el QR)
- En modo superusuario y /config permite cambiar el sexo y eliminar el invitado

Toma num (numero telefonico del invitado como ID)
Toma conf (Verifica si esta /conf y superusuario para mostrar configuraciones)
"""
def invitadoView(request, num, conf=None):
    ingreso = False
    ingresoCancelado = False
    invitado = get_object_or_404(Invitado, numero=num)
    if request.user.is_superuser and not(conf == "config"): #Modo para cambiar a adentro al invitado
        ingreso = True
        invitado.adentro = True #el estado de adentro pasa a ser True
    if not(request.user.is_superuser) or not(conf == "config"): #Modo "normal"
        conf = None
    if request.method == "POST":
        if ("cancelarAdentro" in request.POST) and (request.user.is_superuser) and (conf == "config"):
            Invitado.objects.get(numero=request.POST.get("cancelarAdentro")).adentro = False
            ingresoCancelado = True #En caso de que el patovica haya escaneado por error, puede cancelar el adentro
    elif "sexo" in request.GET: #Cambio de Sexo mediante Ajax
        oldSexo = request.GET.get("sexo")
        print(oldSexo)
        if oldSexo == "H":
            invitado.sexo = "M"
        else:
            invitado.sexo = "H"
        print(invitado.sexo)
        invitado.save() #Guardo nuevo Sexo
        return HttpResponse(json.dumps({"sexo": invitado.sexo}), content_type="application/json") #Devuelvo AjaxRequest
    return render(request, 'invitado.html', {"invitado": invitado, "ingreso": ingreso,
                                             "conf": conf, "host": request.get_host(),
                                             "ingresoCancelado": ingresoCancelado})

"""
adminView
Solo si entras desde una cuenta admin, permite:
- Ver invitados
- Acceder a su wpp
- Ver cantidad de hombres/mujeres
- Añadir invitado

No toma parametros adicionales por url
"""
def adminView(request):
    if not(request.user.is_superuser): #Si no estas logueado como superuser no accedes al admin
        return render(request, "denied.html", {"host": request.get_host()})
    newInvitado = None
    deleteInvitado = None
    if request.method == "POST": #Verifica si desde el invitado/config fue direccionado a esta pag para eliminar
        if "eliminar" in request.POST:
            if len(Invitado.objects.filter(numero=request.POST.get("eliminar"))) != 0:
                invitado = Invitado.objects.get(numero=request.POST.get("eliminar"))
                deleteInvitado = invitado.nombre
                invitado.delete() #Accede al invitado y lo elimina
        else: #Sino, como accede por post es que va a crear un nuevo invitado (Redirrecciono a la misma pag para no usar ajax)
            nombre = request.POST.get("nombre")
            telefono = request.POST.get("telefono")
            sexo = request.POST.get("sexo")
            if len(Invitado.objects.filter(numero=telefono)) == 0:
                newInvitado = Invitado.objects.create(numero=telefono, nombre=nombre, sexo=sexo)
                #Toma los datos pasados por POST y crea el invitado

    invitados = Invitado.objects.all()
    numHombres = len(Invitado.objects.filter(sexo="H"))
    numMujeres = len(Invitado.objects.filter(sexo="M"))
    return render(request, 'admin.html', {'invitados': invitados, 'hombres': numHombres, 'mujeres': numMujeres,
                                         "host": request.get_host(), "newInvitado": newInvitado,
                                         "delInvitado": deleteInvitado
                                         })

"""
smsView
Realiza las logicas para comunicarse con el wppBot
- Crea invitados
- Ofrece asistencia a los invitados como:
    * Pedir su entrada
    * Cambiar su nombre
    * Confirmar inasistencia

No toma parametros adicionales por url
"""
@twilio_view
def smsView(request):
    confirmacion = "Confirmar asistencia al evento en nombre de"
    mensaje_final = "Despues de 60 minutos, la conexion se rompera y tendra que ingresar _join practical-realize_ para reconectar"
    confirmacion_exitosa = "*Confirmacion Exitosa*"
    confirmacion_denegada = "Por favor, ingrese su nombre de nuevo:"
    comando_invalido = "Comando no valido"

    # deleteImgs()
    num = request.POST.get('From')
    if request.POST.get('From') is None:
        r = MessagingResponse()
        r.message("No Number")
        return r
    num = num[9::]
    if len(Invitado.objects.all().filter(numero=num)) == 0:
        invitado = Invitado.objects.create(numero=str(num), nombre=request.POST.get('Body'))
        msg = "¿{} *{}*? \n \n -Si \n -No".format(confirmacion, request.POST.get('Body'))
    else:
        invitado = Invitado.objects.get(numero=num)
        if invitado.confirmado:
            if invitado.cambio_nombre:
                invitado.nombre = request.POST.get('Body')
                invitado.cambio_nombre = False
                invitado.save()
                nombreImagen = genImage(invitado.nombre, str(invitado.id), request.get_host(), str(invitado.numero))
                msg = 'Entrada: http://' + request.get_host() + '/static/invitaciones/' + nombreImagen
                msg += "\n\nNombre cambiado a *{}* exitosamente".format(request.POST.get(
                    'Body')) + '\n\n*Nota*: La tarjeta anterior queda invalida\n\n(Ingrese cualquier cosa para ver acciones)'
                r = MessagingResponse()
                r.message(msg)
                return r

                """
                msg_media = Message()
                # Imagen
                nombreImagen = genImage(invitado.nombre, str(invitado.id), request.get_host(), str(invitado.numero))
                msg_media.media('http://' + request.get_host() + '/static/invitaciones/' + nombreImagen)
                r = MessagingResponse()
                r.nest(msg_media)
                invitado.nombre = request.POST.get('Body')
                invitado.cambio_nombre = False
                invitado.save()
                msg = "Nombre cambiado a *{}* exitosamente".format(request.POST.get(
                    'Body')) + '\n\n*Nota*: La tarjeta anterior queda invalida\n\n(Ingrese cualquier cosa para ver acciones)'
                msg_media.body(msg)

                # msg_media = r.message(msg)
                return r
                """
            elif request.POST.get('Body') == "1":
                nombreImagen = genImage(invitado.nombre, str(invitado.id), request.get_host(), str(invitado.numero))
                msg = 'Entrada: http://' + request.get_host() + '/static/invitaciones/' + nombreImagen + '\n\n(Ingrese cualquier cosa para ver acciones)'
                r = MessagingResponse()
                r.message(msg)
                return r

                """
                r = MessagingResponse()
                msg_media = Message()
                # Imagen
                nombreImagen = genImage(invitado.nombre, str(invitado.id), request.get_host(), str(invitado.numero))
                msg_media.media('http://' + request.get_host() + '/static/invitaciones/' + nombreImagen)
                r.nest(msg_media)
                msg_media.body('(Ingrese cualquier cosa para ver acciones)')
                # msg_media = r.message(msg)
                return r
                """
            elif request.POST.get('Body') == "2":
                msg = "Por favor, ingrese su nombre a cambiar:"
                invitado.cambio_nombre = True
                invitado.save()
            elif request.POST.get('Body') == "3":
                invitado.delete()
                msg = "*Desconfirmacion Exitosa*\n\nVuelva a ingresar su nombre si desea volver a confirmar\n\n{}".format(
                    mensaje_final)
            elif request.POST.get('Body').lower() == "invitados":
                invitados = []
                for invitado in Invitado.objects.all():
                    invitados.append(invitado.nombre)
                invitados.sort()
                invitados_str = '*Lista de invitados*\n'
                for i in range(len(invitados)):
                    invitados_str += "{}. {}\n".format((i + 1), invitados[i])
                msg = invitados_str + '\n(Ingrese cualquier cosa para ver acciones)'
            else:
                msg = "*Acciones Disponibles*\n(Ingrese el numero de accion a realizar) " \
                      "\n \n1. Pedir entrada \n2. Cambiar nombre \n3. Desconfirmar asistencia " \
                      "\n\n{}".format(mensaje_final)
        else:
            if request.POST.get('Body').lower() == "si" or request.POST.get('Body').lower() == "-si":
                invitado.confirmado = True
                invitado.save()
                msg = confirmacion_exitosa

                msg += "\n\n*Acciones Disponibles*\n(Ingrese el numero de accion a realizar) " \
                       "\n \n1. Pedir entrada \n2. Cambiar nombre \n3. Desconfirmar asistencia " \
                       "\n\n{}".format(mensaje_final)

            elif request.POST.get('Body').lower() == "no" or request.POST.get('Body').lower() == "-no":
                msg = confirmacion_denegada
                invitado.delete()
            else:
                msg = "_{}_\n\n¿{} *{}*? \n \n -Si \n -No".format(comando_invalido, confirmacion,
                                                                  invitado.nombre)
    r = MessagingResponse()
    r.message(msg)
    return r
