from django.db import models
from django.contrib.auth.models import User

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
    tipo = models.CharField(max_length=25, choices=TYPE_CHOICES, unique=True, null=True, blank=True, default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE)