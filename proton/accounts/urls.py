from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('', views.home, name='home'),

    # JWT Authentication endpoints
    path('api/token/', views.CsrfExemptObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('unauthorized/', views.unauthorized_view, name='unauthorized'),
    path('redirect_to_home/', views.redirect_to_home, name='redirect_to_home'),
    path('about/', views.about, name='about'),
    path('treatment/', views.treatment, name='treatment'),
    path('contact/', views.contact, name='contact'),
    path('appointment/', views.appointment, name='appointment'),
    path('jwt_login/', views.Home.as_view(), name='jwt_login'),
    path("send-email-form/", views.send_email_form, name="send_email_form"),
    path("send_welcome_email/", views.send_welcome_email, name="send_welcome_email"),
]