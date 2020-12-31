from django.contrib.auth.models import User

def run():
    areas = ['medios_off_line', 'medios_en_tienda', 'e-marketing', 
          'relaciones_publicas', 'mercadotecnia', 'medicion_digital', 'mkt_digital']

    for area in areas:
        print(area[::-1])
        user = User.objects.create_user( username=area, 
        email='antonio.garciar@coppel.com', password=area[::-1])
        user.save()
    print(' Fin de creacion de users')
