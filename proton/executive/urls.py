from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from . import views

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('redirect/', views.role_redirect, name='role_redirect'),
    path('executivehome/', views.executivehome, name='executivehome'),
    path('patients/', views.patient_filter_form, name='patient_filter_form'),
    path('yearly_patients/<int:year>', views.yearly_patients, name='yearly_patients'),
    path('monthly_patients/details/<int:year>/<int:month>', views.monthly_patients, name='monthly_patients'),
]
