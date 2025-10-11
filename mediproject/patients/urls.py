from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register_patient/', views.register_patient, name='register_patient'),
    path('patient_detail/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('all_patients/', views.all_patients, name='all_patients'),
    path('patient/<int:patient_id>/add_prescription/', views.add_prescription, name='add_prescription'),
]
