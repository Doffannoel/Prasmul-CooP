from django.urls import path
from .views import (
    admin_dashboard, landing_page, login_page, register,
    about, features, announcements, faq, contactus, student_dashboard, custom_logout_view, change_password_admin, change_password_mahasiswa
)

urlpatterns = [
    # Landing Page
    path('', landing_page, name='landing_page'),

    # Login Page
    path('login/', login_page, name='login'),
    path('register/', register, name='register'),

    # Static Pages
    path('about/', about, name='about'),
    path('features/', features, name='features'),
    path('announcements/', announcements, name='announcements'),
    path('faq/', faq, name='faq'),
    path('contactus/', contactus, name='contactus'),

    # Dashboard Routes
    path('admin-coop/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('student/dashboard/', student_dashboard, name='student_dashboard'),

    # LogOut
    path('logout/', custom_logout_view, name='logout'),

    # Change Password admin
    path('change-password-admin/', change_password_admin, name='change_password_admin'),

    # Change Password mahasiswa
    path('change-password-mahasiswa/', change_password_mahasiswa, name='change_password_mahasiswa')

]
