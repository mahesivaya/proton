from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('unauthorized/', views.unauthorized_view, name='unauthorized'),
    path('redirect_to_home/', views.redirect_to_home, name='redirect_to_home'),
    path('about/', views.about, name='about'),
    path('treatment/', views.treatment, name='treatment'),
    path('contact/', views.contact, name='contact'),
    path('appointment/', views.appointment, name='appointment')
]