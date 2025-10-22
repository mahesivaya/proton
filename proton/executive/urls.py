from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from . import views

urlpatterns = [
    path('executive_dashboard/', views.executive_dashboard, name='executive_dashboard'),
]