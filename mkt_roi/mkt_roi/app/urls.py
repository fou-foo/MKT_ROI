from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
# agregamos el logout
app_name='app'
urlpatterns = [
 #login basico 
  path('', views.user_login, name='login')  ,
  path('medios_off_line_excel/', views.MKTOffLineExcel.as_view(), name='medios_off_line_excel'), 
  path('menu/', views.Menu, name='menu'),
  path('gracias/', views.Gracias, name='gracias' ) ,
  path('update/<pk>/', views.Update.as_view(), name='update'), 
  path('update/', views.Update.as_view(), name='update'), 
  path('lista_campanias/', views.ListaCampanias, name='lista_campanias'), 
  
  # agregamos el logout
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
