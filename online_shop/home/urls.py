from django.urls import path
from home import views

urlpatterns = [
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('register/',views.register, name='register'),
    path('', views.index,name='home'),
    path('admin/', views.index_admin, name='admin'),
    path('contact/', views.contact, name='contact'),
    path('contact_list/', views.contact_list, name='contact_list'),
    # path('page_not_found/', views.page_not_found, name='page_not_found'),
]