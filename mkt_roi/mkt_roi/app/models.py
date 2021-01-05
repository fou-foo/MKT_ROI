from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

# modelo para asignarle tipo a los usuarios 
class Perfil(models.Model):
    TYPE_CHOICES = (
        ('medios_off_line','medios_off_line'),
        ('medios_en_tienda', 'medios_en_tienda'), 
        ('e-marketing', 'e-marketing'), 
        ('relaciones_publicas', 'relaciones_publicas'),
        ('mercadotecnia', 'mercadotecnia'), 
        ('medicion_digital', 'medicion_digital'), 
        ('mkt_digital', 'mkt_digital') )
    tipo = models.TextField(max_length=25, choices=TYPE_CHOICES, unique=True, null=True, blank=True, default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Campania(models.Model):
    nombre = models.TextField(max_length=100,  null=False)
    area = models.TextField(max_length=25,  null=False)
    usuario_created = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # nunca borremos usuarios 


class Esfuerzo(models.Model):
    #campaña = models.CharField(max_length=60, null=False)
    objetivo_macro = models.TextField(max_length=60, null=False)
    #unidad_de_negocio = models.CharField(max_length=60, null=False)
    segmento = models.TextField(max_length=60, null=False)
    canal = models.TextField(max_length=60, null=False)
    subcanal = models.TextField(max_length=60, null=False)
    inicio = models.DateTimeField('Fecha de inicio de la campaña', null=True)
    fin = models.DateTimeField('Fecha de fin de la campaña', null=True)
    gasto = models.FloatField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    estatus = models.TextField(max_length=2, null=False)
    usuario_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # nunca borremos usuarios 
    campania = models.ForeignKey(Campania, on_delete=models.CASCADE)   
