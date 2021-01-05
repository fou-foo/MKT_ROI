from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
# agregamos el logout
app_name='app'
urlpatterns = [
 #login basico 
  path('', views.user_login, name='login')  ,
  path('medios_off_line_excel/', views.MKTOffLineExcel.as_view(), name='medios_off_line_excel'), 
  path('medios_off_line_form/', views.MKTOffLineForm.as_view(), name='medios_off_line_form'),
  #updatepath('medios_off_line_update/', views.MKTOffLineUpdate.as_view(), name='medios_off_line_update' ) ,
  path('update/<pk>/', views.Update.as_view(), name='update'), 
  path('d/', views.Des.as_view(), name='d'), 

  # agregamos el logout
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
