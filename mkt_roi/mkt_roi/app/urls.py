from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
# agregamos el logout
app_name='app'
urlpatterns = [
 #login basico 
  path('', views.user_login, name='login')  ,
  # vistas que replican los exceles y hacen inserts a la DB
  path('medios_en_tienda_excel/', views.MediosEnTiendaExcel.as_view(), name='medios_en_tienda_excel'), 
  #path('medios_off_line_excel/', views.MKTOffLineExcel.as_view(), name='medios_off_line_excel'), 
  #path('e_marketing_excel/', views.EMarketing.as_view(), name='e_marketing_excel'), 
  #path('relaciones_publicas_excel/', views.RelacionesPublicas.as_view(), name='relaciones_publicas_excel'), 
  #path('mercadotecnia_excel/', views.Mercadotecnia.as_view(), name='mercadotecnia_excel'), 
  path('medicion_digital_excel/', views.MedicionDigital.as_view(), name='medicion_digital_excel'), 
  #path('mkt_digital_excel/', views.MKtDigital.as_view(), name='mkt_digital_excel'), 



  path('menu/', views.Menu, name='menu'),
  path('gracias/', views.Gracias, name='gracias' ) ,
  # este es el interesante
  path('update/<pk>/', views.Update.as_view(), name='update'), 
  path('update/', views.Update.as_view(), name='update'), 

  # nada de interesante 
  path('lista_campanias/', views.ListaCampanias, name='lista_campanias'), 
  
  # agregamos el logout
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
