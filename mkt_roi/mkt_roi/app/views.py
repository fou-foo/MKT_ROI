from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import *
from .forms import LoginForm
import datetime
from django.urls import reverse, reverse_lazy
from django.forms.models import model_to_dict # para parsear facil los modelos 
from django.views.decorators.csrf import csrf_protect

from django.views import View
import numpy as np 
from datetime import datetime


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # intento de redireccion 
                    #return HttpResponse('Authenticated ' 'successfully')
                    return redirect ('app:menu')
 
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})

def Menu(request):
    print('entro al menu')


    if request.user.perfil.tipo in ['medios_en_tienda' ] :#'cenic' :
        return render(request, 'app/medios_en_tienda_index.html', {'form': 1 })
        
    if request.user.perfil.tipo in ['medios_off_line'] : #'cenic' :
        return render(request, 'app/medios_off_line_index.html', {'form': 1 })

    if request.user.perfil.tipo in ['e-marketing'] : #'cenic' :
        return render(request, 'app/e_marketing_index.html', {'form': 1 })

    if request.user.perfil.tipo in ['relaciones_publicas'] : #'cenic' :
        return render(request, 'app/relaciones_publicas_index.html', {'form': 1 })

    if request.user.perfil.tipo in ['mercadotecnia'] : #'cenic' :
        return render(request, 'app/mercadotecnia_index.html', {'form': 1 })

    if request.user.perfil.tipo in ['mkt_digital'] :# 'cenic' 
        return render(request, 'app/mkt_digital_index.html', {'form': 1 })

    if request.user.perfil.tipo in ['medicion_digital'] : #'cenic' 
        return render(request, 'app/medicion_digital_index.html', {'form': 1 })


def Gracias(request):
    print('entro al gracias')
    return render( request, 'app/gracias.html', {'form': 1})

def ListaCampanias(request):
    # solo el usuario que creo las campañas las puede alterar 
    
    campanias = Campania.objects.filter(usuario_created=request.user)
    print('..........')
    campanias_dict = dict()
    print(type(campanias))
    contador=0
    for i in campanias:
        campanias_dict[str(contador)] = model_to_dict(i)
        contador+=1
    print(campanias_dict)
    salida = campanias_dict.values()
    return render(request , 'app/lista_capanias.html', {'campanias': salida, 'n':len(salida)})

   
def formato( forma):
    '''Funcion para parsear la entrada dle POST y preparala para 
    introducirla en la DB en el modeleo definido para cada area 
    NOS SIRVE PARA TODAS LAS AREAS !!!!!!!!!!!!!!!!!!!!'''
    #Objetivos_macro = ['Branding', 'Coppel comunidad', 'Performance', 'Merca Directa', 'Personalización']
    #Retail =  ['Ropa', 'Muebles', 'Zapatos']
    #Segmentos = [ 'Crédito Coppel', 'Préstamo personal', 'Coppel Pay', 'Fondo de retiro', 'Seguros (Club de Protección)',
    #               'Coppel Motos', 'Fashion Market','Comunicación interna', 'Atracción de talento', 'Plan de lealtad']
    Objetivos_macro = ['Branding', 'Coppel comunidad', 'Descargas' ,'Performance', 'Merca Directa', 'Personalización']
    Retail = ['Ropa', 'Muebles', 'Zapatos']
    Segmentos = [ 'Crédito Coppel', 'Préstamo personal', 'Coppel Pay','App Coppel', 'Abonos en línea', 'Fondo de retiro', 'Seguros (Club de Protección)','Coppel Motos', 'Fashion Market','Comunicación interna', 'Atracción de talento',
      'Plan de lealtad','Market Place']
    lista = list(map(lambda x: x.split('.'), forma))
    semimodelo = dict()
    subcanales = list(np.unique( [ x[1] for x in lista ]))
    # EL BUEN CASO
    for s in subcanales:
        for x in lista:
            if s == x[1]:
                semimodelo['subcanal.'+str(s)]= { 'canal' : [x[0]], 
                    'subcanal': [x[1]], 'objetivo_macro' : list(np.unique([ _[2] for _ in lista if _[2] in Objetivos_macro and x[1]== _[1]])), 
                    'segmento' : list(np.unique([_[2] for _ in lista if _[2] in Segmentos+Retail and x[1]== _[1]] ))}
    dict_post = []
    for key, value in semimodelo.items():
        n2 = len(semimodelo[key]['objetivo_macro'])
        n1 = len(semimodelo[key]['segmento'])
        n3 = len(semimodelo[key]['canal'])
        n4 = len(semimodelo[key]['subcanal'])
        for i in range(n2):
            for j in range(n1):
                for k in range(n3):
                    dict_post.append( { 'canal':semimodelo[key]['canal'][k] ,'subcanal' : semimodelo[key]['subcanal'][0], 
              'objetivo_macro': semimodelo[key]['objetivo_macro'][i], 'segmento': semimodelo[key]['segmento'][j]
             })
    semimodelo= {}
    for i in range(len(dict_post)):
       semimodelo[str(i)] = dict_post[i]
        
    return(semimodelo)


def insert_db_default(post_request):
    bolsa = post_request.POST
    forma = {}
    #print(bolsa )
    campaña = ''
    for x in bolsa.keys():
        if x not in  ['csrfmiddlewaretoken' , 'campaña'] :
            forma[x] = bolsa[x]
        if x == 'campaña':
                campaña = bolsa[x]
    campaña_insert = Campania(nombre=campaña, usuario_created=post_request.user, area=post_request.user.perfil.tipo )
    campaña_insert.save()
    forma = list(forma.keys())
    forma = formato(forma)
    for key, value in forma.items():
        #print('...................')
        #print(value)
        #print(key)
        insert_esfuerzo =Esfuerzo(objetivo_macro=value['objetivo_macro'], segmento=value['segmento'], canal=value['canal'],
            subcanal=value['subcanal'], inicio=None, fin=None, gasto=None, estatus='P', 
            usuario_updated=post_request.user, campania=campaña_insert )
        insert_esfuerzo.save()
    #print('todos los insert chidos')
    #print(forma.values())
    return(campaña_insert.id)
 


class Update(View):
    
    def get(self, request, pk):
        print('entro   update get                    ------------------------------')
        for i in request.GET  :
            print(i)
        campaña = Campania.objects.get(pk =pk)
        form = dict()
        esfuerzos_pendientes = Esfuerzo.objects.filter(campania=campaña, estatus='P') 
        contador=0
        for i in esfuerzos_pendientes:
            form[str(contador)] = model_to_dict(i)
            contador+=1
        print('valores viejos ')
        return render(request, 'app/update.html', {'esfuerzos':form.values() , 'campania': campaña.nombre ,'campania_id': campaña.id })

    def post(self, request):
        ''' actualizacion de los valors en la DB ''' 
        #print( 'entro al post ')
        bolsa = dict(request.POST)
        util = dict()
        print(bolsa)
        # update a la DB VAMOS A APROVECHAR QUE EN EM POST DEL HTML YA ENVIAMOS ORDENADOS LOS ELEMENTOS !!!!!!!!!!
        for k, values  in bolsa.items():
            if k in ['id', 'gasto']:
                util[k] = list( map(lambda x: float(x), values) )
            if k in ['inicio', 'fin']:
                util[k] = list(map(lambda x: datetime.strptime(x, '%Y-%m-%d').date(), values ) )
        #print(util)
        for n in range(len(util['id'])):
            # vamos ha hacer el update de uno por uno, porque en cenic tenemos recursos super limitados si algun dia tenemos mas checar etsa referencia
            # # https://stackoverflow.com/questions/3221938/difference-between-djangos-filter-and-get-methods 
            #print(' adnamos actualizando')
            id = int(util['id'][n])
            esfuerzo = Esfuerzo.objects.get(pk=id)
            esfuerzo.inicio = util['inicio'][n]
            esfuerzo.fin = util['fin'][n]
            esfuerzo.gasto = util['gasto'][n]
            esfuerzo.updated= datetime.now()
            esfuerzo.usuario_updated=request.user   
            esfuerzo.save()
        print('se updeteo todo ')
        return redirect( 'app:gracias')



class MKTOffLineExcel(View):
    ''' esta vista se encarga de construir el excel donde mapeamos los esfuerzos de las areas es fundamental para el proyecto
    ademas en el post insertamos los registros en las tablas con algunos campos en blanco que despues actualizamos en la vista update'''
    
    def get(self, request):
        ''' construiccion de la vista del excel ''' 
        print('entro al excel get ')
        return render(request, 'app/medios_off_line_excel.html', {'form': 1 })

    def post(self, request):
        ''' insert a la DB''' 
        print(' post excel ')
        if request.user.perfil.tipo in ['medios_off_line' , 'cenic']:
            pk=insert_db_default(request)
            return redirect( 'app:update', pk=pk)
        else  :
            return render(request, 'app/login.html', {'form': 1 })
 
class MediosEnTiendaExcel(View):
    ''' esta vista se encarga de construir el excel donde mapeamos los esfuerzos de las areas es fundamental para el proyecto
    ademas en el post insertamos los registros en las tablas con algunos campos en blanco que despues actualizamos en la vista update'''
    
    def get(self, request):
        ''' construiccion de la vista del excel ''' 
        print('entro al excel get ')
        return render(request, 'app/medios_en_tienda_excel.html', {'form': 1 })

    def post(self, request):
        ''' insert a la DB''' 
        print(' post excel ')
        if request.user.perfil.tipo in ['medios_en_tienda' , 'cenic']:
            pk=insert_db_default(request)
            return redirect( 'app:update', pk=pk)
        else  :
            return render(request, 'app/login.html', {'form': 1 })


class EMarketing(View):
    ''' esta vista se encarga de construir el excel donde mapeamos los esfuerzos de las areas es fundamental para el proyecto
    ademas en el post insertamos los registros en las tablas con algunos campos en blanco que despues actualizamos en la vista update'''
    
    def get(self, request):
        ''' construiccion de la vista del excel ''' 
        print('entro al excel get ')
        return render(request, 'app/e_marketing_excel.html', {'form': 1 })

    def post(self, request):
        ''' insert a la DB e-marketing''' 
        print(' post excel ')
        if request.user.perfil.tipo in ['e-marketing' , 'cenic']:
            pk=insert_db_default(request)
            return redirect( 'app:update', pk=pk)
        else  :
            return render(request, 'app/login.html', {'form': 1 })

class RelacionesPublicas(View):
    ''' esta vista se encarga de construir el excel donde mapeamos los esfuerzos de las areas es fundamental para el proyecto
    ademas en el post insertamos los registros en las tablas con algunos campos en blanco que despues actualizamos en la vista update'''
    
    def get(self, request):
        ''' construiccion de la vista del excel ''' 
        print('entro al excel getrel publicas ')
        return render(request, 'app/relaciones_publicas_excel.html', {'form': 1 })

    def post(self, request):
        ''' insert a la DB''' 
        print(' post excel ')
        if request.user.perfil.tipo in ['relaciones_publicas' , 'cenic']:
            pk=insert_db_default(request)
            return redirect( 'app:update', pk=pk)
 
class Mercadotecnia(View):
    ''' esta vista se encarga de construir el excel donde mapeamos los esfuerzos de las areas es fundamental para el proyecto
    ademas en el post insertamos los registros en las tablas con algunos campos en blanco que despues actualizamos en la vista update'''
    
    def get(self, request):
        ''' construiccion de la vista del excel ''' 
        print('entro al excel get mercadotecnia')
        return render(request, 'app/mercadotecnia_excel.html', {'form': 1 })

    def post(self, request):
        ''' insert a la DB''' 
        print(' post excel  mercadotecnia')
        print(' post excel ')
        if request.user.perfil.tipo in ['mercadotecnia' , 'cenic']:
            pk=insert_db_default(request)
            return redirect( 'app:update', pk=pk)

class MedicionDigital(View):
    ''' esta vista se encarga de construir el excel donde mapeamos los esfuerzos de las areas es fundamental para el proyecto
    ademas en el post insertamos los registros en las tablas con algunos campos en blanco que despues actualizamos en la vista update'''
    
    def get(self, request):
        ''' construiccion de la vista del excel ''' 
        print('entro al excel get medicion digital')
        return render(request, 'app/medicion_digital_excel.html', {'form': 1 })

    def post(self, request):
        ''' insert a la DB''' 
        print(' post excel medicion digital')
        if request.user.perfil.tipo in ['medicion_digital' , 'cenic']:
            pk=insert_db_default(request)
            return redirect( 'app:update', pk=pk)

class MKtDigital(View):
    ''' esta vista se encarga de construir el excel donde mapeamos los esfuerzos de las areas es fundamental para el proyecto
    ademas en el post insertamos los registros en las tablas con algunos campos en blanco que despues actualizamos en la vista update'''
    
    def get(self, request):
        ''' construiccion de la vista del excel ''' 
        print('entro al excel get mkt digital')
        return render(request, 'app/mkt_digital_excel.html', {'form': 1 })

    def post(self, request):
        ''' insert a la DB''' 
        print(' post excel mkt digital')
        if request.user.perfil.tipo in ['mkt_digital' , 'cenic']:
            pk=insert_db_default(request)
            return redirect( 'app:update', pk=pk)
