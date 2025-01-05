from django.urls import path
from .views import student_list, admin_profile, student_profile, company_data, grafik_view, send_supervisor_email
from userauths.views import add_student

urlpatterns = [
    path('admin-dashboard/', student_list, name='admin_dashboard'),  # Pastikan mengarah ke student_list
    path('studentlist/', student_list, name='student_list'),
    path('add_student/', add_student, name='add_student'),
    path('admin-profile/', admin_profile, name='admin_profile'),
    path('student/<str:nim>/profile/', student_profile, name='student_profile'),
    path('student/<str:nim>/company/', company_data, name='company_data'),
    path('dashboard/grafik/', grafik_view, name='grafik_page'),
    path('send-email-supervisor/<int:company_id>/', send_supervisor_email, name='send_supervisor_email'),
    # path('mahasiswa_belum_mengisi_form/', mahasiswa_belum_mengisi_form, name='mahasiswa_belum_mengisi_form'),
]