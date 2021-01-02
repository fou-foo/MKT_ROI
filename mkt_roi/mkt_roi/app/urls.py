from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
# agregamos el logout
from django.contrib.auth import views as auth_views
 
app_name='app'
urlpatterns = [
 #login basico 
  path('', views.user_login, name='login')  ,
  path('medios_off_line_excel', views.MKTOfflineExcel.as_view(), name='medios_off_line_excel'), 


  # agregamos el logout
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
