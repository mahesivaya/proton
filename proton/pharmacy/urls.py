from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from . import views as views

urlpatterns = [
    path('pharmacy_home/', views.pharmacy_dashboard, name='pharmacy_dashboard'),
    path('inventory/', views.inventory_dashboard, name='inventory_dashboard'),
]
