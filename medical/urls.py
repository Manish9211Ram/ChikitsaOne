from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.patient_register, name='register'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('services/', views.service_list, name='service_list'),
    path('appointment/search/', views.book_appointment_search, name='appointment_search'),
    path('appointment/select/', views.book_appointment_select, name='book_appointment_select'),
    path('doctor/login/', views.doctor_login, name='doctor_login'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('records/', views.all_records, name='all_records'),
    path('patient/update/search/', views.update_patient_search, name='update_patient_search'),
    path('patient/update/form/', views.update_patient_form, name='update_patient_form'),
]
