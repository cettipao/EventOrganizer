from django.contrib import admin
from .models import *

# Register your models here.

class InvitadoAdmin(admin.ModelAdmin):
    list_display = ['numero','nombre','sexo','confirmado']    
    list_display_links = ['numero','nombre','sexo','confirmado']

    fieldsets = (
        ('Datos', {
          'fields': ('numero','nombre','sexo')  
        }),
        ('Extra', {
            'fields': ('confirmado','cambio_nombre',)
        }),
    )

admin.site.register(Invitado,InvitadoAdmin)