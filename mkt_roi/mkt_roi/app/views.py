from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import *
from .forms import LoginForm
import datetime
from django.forms import formset_factory 
from django.urls import reverse, reverse_lazy
from django.forms.models import model_to_dict # para parsear facil los modelos 
from django.views.decorators.csrf import csrf_protect

from django.views import View
import numpy as np 

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
                    if request.user.perfil.tipo=='medios_off_line':
                        #ver https://stackoverflow.com/questions/49092710/django-redirect-user-to-different-page-by-users-type
                        #return redirect(  'offline' )
                        return render(request, 'app/medios_off_line_index.html', {'form': form })
                    if  request.user.perfil.tipo=='medios_en_tienda':
                        return render(request, 'app/medios_en_tienda_index.html', {'form': form })
 
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})

class MKTOffLineExcel(View):
    
    def get(self, request):
        return render(request, 'app/medios_off_line_excel.html', {'form': 1 })

    def post(self, request):
        if request.user.perfil.tipo=='medios_off_line':
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
            forma = self.formato(forma)
            
            for key, value in forma.items():
                insert_esfuerzo =Esfuerzo(objetivo_macro=value['objetivo_macro'], segmento=value['segmento'], canal=value['canal'],
                 subcanal=value['subcanal'], inicio=None, fin=None, gasto=None, estatus='P', 
                 usuario_updated=request.user, campania=campaña_insert )
                insert_esfuerzo.save()
            #print(' ----*************----------- ')
            #print(forma.values())
            print('todos los inserts chidos  '   )
            print(campaña_insert.id)
            #return  render(request, 'app/medios_off_line_form.html', {'form' : forma.values()})
            return redirect( 'app:update', pk=campaña_insert.id)
        else  :
            return render(request, 'app/login.html', {'form': 1 })
    
    def formato(self,  forma):
        '''Funcion para parsear la entrada dle POST y preparala para 
        introducirla en la DB en el modeleo definido para acada area '''
        Objetivos_macro = ['Branding', 'Coppel comunidad', 'Performance', 'Merca Directa', 'Personalización']
        Retail =  ['Ropa', 'Muebles', 'Zapatos']
        Segmentos = [ 'Crédito Coppel', 'Préstamo personal', 'Coppel Pay', 'Fondo de retiro', 'Seguros (Club de Protección)',
                       'Coppel Motos', 'Fashion Market','Comunicación interna', 'Atracción de talento', 'Plan de lealtad']
        
        lista = list(map(lambda x: x.split('.'), forma))
        #print('-------lista')
        #print(lista)
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
        print('mmmmmmmmmmmmmmmmmm al get llave pk ')
        print(pk)
        campaña = Campania.objects.get(pk =pk)
        print(campaña.id)
        print('esfuerzos')
        esfuerzos_pendientes = Esfuerzo.objects.filter(campania=campaña, estatus='P') 
        print(type(esfuerzos_pendientes))
        form = { model_to_dict(i)  for i in esfuerzos_pendientes }
        print(form)
        return render(request, 'app/update.html', {'form':1 })

        #return render(request, 'app/medios_off_line_excel.html', {'form': 1 })

class MKTOffLineForm(View):
    
    def get(self, request):
        print('entro                       ')
        print(request)
        #campaña_id = request.GET.get('compania_id')
        print('mmmmmmmmmmmmmmmmmm')
        #print(campaña_id)
        #campaña = Campania.objects.get(pk =campaña_id)
        #esfuerzos_pendientes = Esfuerzo.objects.filter(campania=campaña, estatus='P') 
        #form = { model_to_dict(i)  for i in esfuerzos_pendientes }
        return render(request, 'app/login.html', {'form':1 })

class Des(View):
    
    def get(self, request):
        return render(request, 'app/medios_off_line_excel.html', {'form': 1 })

    def post(self, request):
        if request.user.perfil.tipo=='medios_off_line':
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
            forma = self.formato(forma)
            
            print(' ----*************----------- ')
            print(forma.values())
            print('todos los inserts chidos  '   )
            print(campaña_insert.id)
            #return  render(request, 'app/medios_off_line_form.html', {'form' : forma.values()})
            return render( request, 'app/medios_off_line_form2.html', {'form':forma.values() , 'campania' : campaña_insert.nombre} )
        else  :
            return render(request, 'app/login.html', {'form': 1 })
    
    def formato(self,  forma):
        '''Funcion para parsear la entrada dle POST y preparala para 
        introducirla en la DB en el modeleo definido para acada area '''
        Objetivos_macro = ['Branding', 'Coppel comunidad', 'Performance', 'Merca Directa', 'Personalización']
        Retail =  ['Ropa', 'Muebles', 'Zapatos']
        Segmentos = [ 'Crédito Coppel', 'Préstamo personal', 'Coppel Pay', 'Fondo de retiro', 'Seguros (Club de Protección)',
                       'Coppel Motos', 'Fashion Market','Comunicación interna', 'Atracción de talento', 'Plan de lealtad']
        
        lista = list(map(lambda x: x.split('.'), forma))
        #print('-------lista')
        #print(lista)
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


def d(request):
    return render( request, 'app/medios_off_line_form.html', )



class MKTOfflineExcel_s(View):
    def get(self, request):
        if request.user.perfil.tipo=='medios_off_line':

            #ver https://stackoverflow.com/questions/50595330/django-bulk-create-createview
                        # LO ADAPTE 
            return render(request, 'app/medios_off_line_excel.html', {'form': 1 })
        else  :
            return render(request, 'app/login.html', {'form': 1 })
    def post(self, request):
        bolsa = request.POST #.get('exceldata')
        forma = {}
        for x in bolsa.keys():
            if x != 'csrfmiddlewaretoken' :
                forma[x] = bolsa[x]
        forma = list(forma.keys())
        print('--------------')
        
        forma = self.formato(forma)
        
        if request.user.perfil.tipo=='medios_off_line':
            return render(request, 'app/medios_off_line_form.html', {'form': sorted(forma.items()) })
        else  :
            return render(request, 'app/login.html', {'form': 1 })
    
    def formato(self, forma):
        '''Funcion para parsear la entrada dle POST y preparala para 
        introducirla en la DB en el modeleo definido para acada area '''
        Objetivos_macro = ['Branding', 'Coppel comunidad', 'Performance', 'Merca Directa', 'Personalización']
        Retail =  ['Ropa', 'Muebles', 'Zapatos']
        Segmentos = [ 'Crédito Coppel', 'Préstamo personal', 'Coppel Pay', 'Fondo de retiro', 'Seguros (Club de Protección)',
                       'Coppel Motos', 'Fashion Market','Comunicación interna', 'Atracción de talento', 'Plan de lealtad']
    
        lista = list(map(lambda x: x.split('.'), forma))
        print(lista)
        semimodelo = dict()
        subcanales = list(np.unique( [ x[1] for x in lista ]))
        canales = list(np.unique( [ x[0] for x in lista ]))
        # EL BUEN CASO
        for s in subcanales:
            for x in lista:
                if s == x[1]:
                    semimodelo['subcanal.'+str(s)]= { 'canal' : x[0], 
                    'subcanal': x[1], 'objetivo_macro' : [ _[2] for _ in lista if _[2] in Objetivos_macro and x[1]== _[1]], 
                    'segmento' : [_[2] for _ in lista if _[2] in Segmentos+Retail and x[1]== _[1]]}
        print('...................')
        print(semimodelo)
        return ( semimodelo)


def update(request):
    if request.user.perfil.tipo=='medios_off_line':
        return render(request, 'app/medios_off_line_update.html', {'form': 1 })
    else  :
        return render(request, 'app/login.html', {'form': 1 })

def MKTOfflineView_s(request):
    if request.method == "POST":
        #n_rows = sum(# el numero de inserts que se van a hacer  HAY QUE CHECAR ESTO PORQUE  NO SE DEFINIO BIEN ESTE REQUERIMIENTO, PUEDE DARSE 
        # EL CASO DE QUE UNA MISMA CAMPAÑA SE DESCONOZCA EL NUMERO DE CANALES QUE UTILIZO POR ANTICIPADO PREGUNTAR A FERNANDOI VILLA PARA QUE LO SOLUCIONE
        forms = [    MKTOfflineView(dict(campaña=c, objetivo_macro=om, 
        segmento=s, canal=c, subcanal=subc, inicio=i, fin=f, gasto=g, 
        created = ct, updated=ut))  for c, om, s, c, subc, i, f, g, ct, ut in zip(
                request.POST.getlist("campaña"),
                request.POST.getlist("objetivo"),
                request.POST.getlist("canal"),
                request.POST.getlist("subcanal"),
                request.POST.getlist("inicio"), 
                request.POST.getlist("fin"),
                request.POST.getlist("gasto"), 
                datetime.datetime.now(), 
                datetime.datetime.now()
            )
        ]
        if all(forms[i].is_valid() for i in range(len(forms))):                
            for form in forms:
                form.save() 
            return HttpResponse(
                f"success to create {len(forms)} Schedule instances."
            )
    else:
        forms = [MKTOfflineForm() for _ in range(3)]
    return render(request, "app/medios_off_line_form.html", {"forms": forms})


