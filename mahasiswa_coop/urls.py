from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path('company_form/', views.company_form, name='company_form'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),  
    path('upload_laporan/', views.upload_laporan, name='upload_laporan'),
    # path('logout/', views.logout_view, name='logout'),
]