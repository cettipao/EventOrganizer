from django.contrib import admin
from .models import *

# Register your models here.

class InvitadoAdmin(admin.ModelAdmin):
    list_display = ['numero','nombre','sexo','mesa']
    list_display_links = ['numero','nombre','sexo','mesa']
    search_fields = ['nombre', 'numero']
    list_filter = ('sexo', 'mesa',)

    fieldsets = (
        ('Datos', {
          'fields': ('numero','nombre','sexo')
        }),
        ('Extra', {
            'fields': ('mesa',)
        }),
    )
    actions = ['make_hombre','make_mujer']
    def make_hombre(self, request, queryset):
        return queryset.update(sexo="H")

    def make_mujer(self, request, queryset):
        return queryset.update(sexo="M")

class InvitadoInLine(admin.TabularInline): #Para ver los prestamos de la persona
    model = Invitado

class MesaAdmin(admin.ModelAdmin):
    inlines = [InvitadoInLine, ]
    list_display = ('numero_mesa', 'isInfantil')

admin.site.register(Invitado,InvitadoAdmin)
admin.site.register(Mesa, MesaAdmin)
admin.site.register(Ingreso)