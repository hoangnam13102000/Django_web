from django.urls import path
from home import views

urlpatterns = [
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('register/',views.register, name='register'),
    path('', views.index,name='home'),
    path('index_admin/', views.index_admin, name='index_admin'),
    path('contact/', views.contact, name='contact'),
    path('contact_list/', views.contact_list, name='contact_list'),
]