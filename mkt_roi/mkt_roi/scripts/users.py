from django.contrib.auth.models import User
from app.models import Perfil 
def run():
    tipo = ['medios_off_line', 'medios_en_tienda', 'e-marketing', 'relaciones_publicas',  'mercadotecnia' ,
            'medicion_digital' , 'mkt_digital' , 'cenic' ]
    for area in tipo:
        print(area[::-1])
        user = User.objects.create_user( username=area, 
        email='antonio.garciar@coppel.com', password=area[::-1])
        user.save()
        perfil = Perfil(tipo=area, user=user)
        perfil.save()
        

    print(' Fin de creacion de users')
