from django.http import HttpResponse
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import MKTOffLine
from .forms import LoginForm, MKTOfflineForm
import datetime

from django.views import View


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



from django.views.decorators.csrf import csrf_protect

class MKTOfflineExcel(View):
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
        print(forma)
        #return redirect(request.path)
        if request.user.perfil.tipo=='medios_off_line':
            return render(request, 'app/medios_off_line_form.html', {'form': forma })
        else  :
            return render(request, 'app/login.html', {'form': 1 })




#def MKTOfflineExcel(request):
#    if request.user.perfil.tipo=='medios_off_line':
        #ver https://stackoverflow.com/questions/50595330/django-bulk-create-createview
                        # LO ADAPTE 
 #       return render(request, 'app/medios_off_line_excel.html', {'form': 1 })
  #  else  :
   #     return render(request, 'app/login.html', {'form': 1 })

@csrf_protect
def MKTOfflineForm(request):
    if request.user.perfil.tipo=='medios_off_line':
        #ver https://stackoverflow.com/questions/50595330/django-bulk-create-createview
                        # LO ADAPTE 
        return render(request, 'app/medios_off_line_form.html', {'form': request.excelform })
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