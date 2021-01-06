from django.contrib.auth.models import User
from app.models import Perfil 
def run():
    tipo = ['medios_off_line', 'medios_en_tienda', 'e-marketing', 'relaciones_publicas',  'mercadotecnia' ,
            'medicion_digital' , 'mkt_digital' , 'cenic' ]
    for area in tipo:
        print(area[::-1])
        user = Perfil.objects.create_user( username=area, email='antonio.garciar@coppel.com', password=area[::-1], tipo=area )
        user.save()
       
    print(' Fin de creacion de users')
