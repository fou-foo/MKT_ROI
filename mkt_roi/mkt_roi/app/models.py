from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

# modelo para asignarle tipo a los usuarios 
class Perfil(models.Model):
    tipo = models.CharField(max_length=25, null=False)
    user  = models.ForeignKey(User, on_delete=models.CASCADE) # nunca borremos usuarios 
    
    def __str__(self):
        return self.tipo
    

class Campania(models.Model):
    nombre = models.CharField(max_length=100,  null=False)
    area = models.CharField(max_length=25,  null=False)
    usuario_created = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # nunca borremos usuarios 

    def __str__(self):
        return self.nombre


class Esfuerzo(models.Model):
    #campaña = models.CharField(max_length=60, null=False)
    objetivo_macro = models.CharField(max_length=60, null=False)
    #unidad_de_negocio = models.CharField(max_length=60, null=False)
    segmento = models.CharField(max_length=60, null=False)
    canal = models.CharField(max_length=60, null=False)
    subcanal = models.CharField(max_length=60, null=False)
    inicio = models.DateField('Fecha de inicio de la campaña', null=True)
    fin = models.DateField('Fecha de fin de la campaña', null=True)
    gasto = models.FloatField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    estatus = models.CharField(max_length=2, null=False)
    usuario_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # nunca borremos usuarios 
    campania = models.ForeignKey(Campania, on_delete=models.CASCADE)   

    def __str__(self):
        return self.subcanal