from django.http import HttpResponse
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm


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