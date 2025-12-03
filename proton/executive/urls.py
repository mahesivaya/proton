from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from . import views

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('patients/', views.patient_filter_form, name='patient_filter_form'),
    path('yearly_patients/<int:year>', views.yearly_patients, name='yearly_patients'),
    path('monthly_patients/details/<int:year>/<int:month>', views.monthly_patients, name='monthly_patients'),
]