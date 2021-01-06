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
    if request.user.perfil.tipo=='medios_off_line' or request.user.perfil.tipo=='cenic' :
        return render(request, 'app/medios_off_line_index.html', {'form': 1 })

def Gracias(request):
    return render( request, 'app/gracias.html', {'form': 1})

def ListaCampanias(request):
    # solo el usuario que creo las campañas las puede alterar 
    campanias = dict(Campania.objects.filter(usuario_created=request.user))
    return render( 'app:lista_capanias.html', {'campanias': campanias})

    #  campaña = Campania.objects.get(pk =pk)
        #print('esfuerzos...................')
    #    form = dict()
    #    esfuerzos_pendientes = Esfuerzo.objects.filter(campania=campaña, estatus='P') 
    #    contador=0
    #    for i in esfuerzos_pendientes:
    #        form[str(contador)] = model_to_dict(i)
    #        contador+=1
  



class MKTOffLineExcel(View):
    ''' esta vista se encarga de construir el excel donde mapeamos los esfuerzos de las areas es fundamental para el proyecto
    ademas en el post insertamos los registros en las tablas con algunos campos en blanco que despues actualizamos en la vista update'''
    
    def get(self, request):
        ''' construiccion de la vista del excel ''' 
        return render(request, 'app/medios_off_line_excel.html', {'form': 1 })

    def post(self, request):
        ''' insert a la DB''' 
        if request.user.perfil.tipo in ['medios_off_line' , 'cenic']:
            bolsa = request.POST
            forma = {}
            campaña = ''
            for x in bolsa.keys():
                if x not in  ['csrfmiddlewaretoken' , 'campaña'] :
                    forma[x] = bolsa[x]
                if x == 'campaña':
                    campaña = bolsa[x]
            campaña_insert = Campania(nombre=campaña, usuario_created=request.user, area=request.user.perfil.tipo )
            campaña_insert.save()
            forma = list(forma.keys())
            forma = formato(forma)
            for key, value in forma.items():
                insert_esfuerzo =Esfuerzo(objetivo_macro=value['objetivo_macro'], segmento=value['segmento'], canal=value['canal'],
                 subcanal=value['subcanal'], inicio=None, fin=None, gasto=None, estatus='P', 
                 usuario_updated=request.user, campania=campaña_insert )
                insert_esfuerzo.save()
            print('todos los inserts chidos  '   )
            print(forma)
            return redirect( 'app:update', pk=campaña_insert.id)
        else  :
            return render(request, 'app/login.html', {'form': 1 })
    
def formato( forma):
    '''Funcion para parsear la entrada dle POST y preparala para 
    introducirla en la DB en el modeleo definido para acada area 
    NOS SIRVE PARA TODAS LAS AREAS !!!!!!!!!!!!!!!!!!!!'''
    Objetivos_macro = ['Branding', 'Coppel comunidad', 'Performance', 'Merca Directa', 'Personalización']
    Retail =  ['Ropa', 'Muebles', 'Zapatos']
    Segmentos = [ 'Crédito Coppel', 'Préstamo personal', 'Coppel Pay', 'Fondo de retiro', 'Seguros (Club de Protección)',
                   'Coppel Motos', 'Fashion Market','Comunicación interna', 'Atracción de talento', 'Plan de lealtad']
    
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


class Update(View):
    
    def get(self, request, pk):
        print('entro                       ------------------------------')
        for i in request.GET  :
            print(i)
        #campaña_id = request.GET.get('compania_id')
        #print('mmmmmmmmmmmmmmmmmm al get llave pk ')
        #print(pk)
        campaña = Campania.objects.get(pk =pk)
        #print('esfuerzos...................')
        form = dict()
        esfuerzos_pendientes = Esfuerzo.objects.filter(campania=campaña, estatus='P') 
        contador=0
        for i in esfuerzos_pendientes:
            form[str(contador)] = model_to_dict(i)
            contador+=1
        
        #print(form)
        return render(request, 'app/update.html', {'esfuerzos':form.values() , 'campania': campaña.nombre ,'campania_id': campaña.id })

    def post(self, request):
        ''' actualizacion de los valors en la DB ''' 
        #print( 'entro al post ')
        bolsa = dict(request.POST)
        util = dict()
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

        #return render(request, 'app/medios_off_line_excel.html', {'form': 1 })
