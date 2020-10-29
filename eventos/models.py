from django.db import models

# Create your models here.


class Mesa(models.Model):
    numero_mesa = models.IntegerField()
    infantil = models.BooleanField()

    def isInfantil(self):
        return self.infantil
    isInfantil.boolean = infantil
    isInfantil.short_description = 'Mesa de Niños'

    def __str__(self):
        return "{}".format(self.numero_mesa)

class Invitado(models.Model):
    numero = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30, null=True, blank=True)
    sexos = [
        ("H", 'Hombre'),
        ("M", 'Mujer'),
    ]
    sexo = models.CharField(
        max_length=2,
        choices=sexos,
        blank=True,
    )
    mesa = models.ForeignKey(
        'Mesa',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    confirmado = models.BooleanField(default = False)
    cambio_nombre = models.BooleanField(default=False)

    def __str__(self):
        return "{}, {}".format(self.numero, self.nombre)

class Ingreso(models.Model):
    invitado = models.OneToOneField(
        'Invitado',
        on_delete=models.CASCADE,
        null=False
    )
    hora = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}, {}".format(self.invitado.nombre, self.hora.ctime())