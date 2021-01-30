from django.contrib.auth.models import User
from app.models import Perfil 
def run():
    tipo = ['medios_off_line', 'medios_en_tienda', 'e-marketing', 'relaciones_publicas',  'mercadotecnia' ,
            'medicion_digital' , 'mkt_digital' , 'cenic' ]

    nombre = [ 'Jorge Luis',       'Jazmín',    'Frank',           'Andrea' ,      'Juan David', 
                'Víctor Hugo',  'Arturo', 'Dulce'] # cuidar orden con areas

    apellido = [ 'Loaiza',          'Izabal',   ' Astorga',          'Parra' ,    'González',
                 'Estrada Bello', 'Muñoz' , 'Magaña']         # cuidar orden con areas

    for i in range(len(tipo)) :
        area = tipo[i]
        print(area[::-1])
        user = Perfil.objects.create_user( username=area, email='christian.barradas@coppel.com', password=area[::-1], tipo=area , first_name=nombre[i], 
        last_name=apellido[i] )
        user.save()
       
    print(' Fin de creacion de users')
