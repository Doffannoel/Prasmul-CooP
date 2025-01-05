from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CustomPasswordChangeForm, LoginForm, MahasiswaRegistrationForm
import logging
from django.contrib.auth import logout
from django.contrib import messages

# Landing Page
def landing_page(request):
    return render(request, 'userauths/index.html')

# Static Pages
def about(request):
    return render(request, 'about.html')

def features(request):
    return render(request, 'features.html')

def announcements(request):
    return render(request, 'announcements.html')

def faq(request):
    return render(request, 'faq.html')

def contactus(request):
    return render(request, 'contactus.html')

logger = logging.getLogger(__name__)

def login_page(request):
    form = LoginForm()  # Inisialisasi form
    if request.method == 'POST':
        form = LoginForm(data=request.POST)  # Masukkan data POST ke form
        if form.is_valid():
            logger.info("Form is valid.")
            # Ambil user berdasarkan email yang di-submit
            user = authenticate(
                request,
                email=form.cleaned_data['username'],  # Gunakan email sebagai 'username'
                password=form.cleaned_data['password']
            )
            if user:
                logger.info(f"User {user.email} authenticated successfully.")
                login(request, user)
                # Redirect berdasarkan role user
                if user.is_admin_coop:
                    logger.info("Redirecting to admin dashboard.")
                    return redirect('admin_dashboard')  # Admin ke dashboard admin
                elif user.is_student:
                    logger.info("Redirecting to student dashboard.")
                    return redirect('student_dashboard')  # Mahasiswa ke dashboard mahasiswa
                else:
                    logger.info("Redirecting to landing page.")
                    return redirect('landing_page')  # Default redirect jika role tidak dikenali
            else:
                logger.warning("Authentication failed.")
                form.add_error(None, 'Invalid username or password')  # Tambahkan error jika user tidak valid
        else:
            logger.warning("Form is invalid.")

    return render(request, 'userauths/login.html', {'form': form})


# Admin Co-op Dashboard
@login_required
def admin_dashboard(request):
    if request.user.is_admin_coop:
        return render(request, 'admin_coop/studentlist.html')  # Dashboard Admin Co-op
    return redirect('landing_page')  # Jika bukan admin co-op

# Student Dashboard
@login_required
def student_dashboard(request):
    if request.user.is_student:
        return render(request, 'student/dashboard.html')  # Dashboard Mahasiswa
    return redirect('landing_page')  # Jika bukan mahasiswa


def custom_logout_view(request):
    # Add any custom logic here (e.g., logging actions)
    logout(request)
    return redirect('landing_page')  # Replace 'index' with your landing page URL name

CustomUser = get_user_model()

def register(request):
    if request.method == 'POST':
        form = MahasiswaRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Simpan data form dan profil mahasiswa
            form.save()
            messages.success(request, "Registrasi berhasil! Silakan login.")
            return redirect('login')  # Ganti dengan URL login Anda
        else:
            messages.error(request, "Registrasi gagal. Periksa kembali data yang dimasukkan.")
            print(f"Form is invalid. Errors: {form.errors}")  # Debugging
    else:
        form = MahasiswaRegistrationForm()

    return render(request, 'userauths/register.html', {'form': form})


#Function Change password untuk admin dan mahasiswa
@login_required
def change_password_admin(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            # Simpan password baru
            form.save()
            # Perbarui sesi pengguna agar tidak ter-logout
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password berhasil diubah!')

            # Cek role pengguna dan arahkan ke halaman yang sesuai
            if request.user.is_staff:  # Admin
                return redirect('profileadmin')  # Ganti 'admin_dashboard' dengan nama URL untuk dashboard admin
            else:  # Mahasiswa
                return redirect('student_dashboard')  # Ganti 'student_dashboard' dengan nama URL untuk dashboard mahasiswa

        else:
            messages.error(request, 'Terdapat kesalahan. Periksa kembali input Anda.')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'userauths/change_password_admin.html', {'form': form})

#Function Change password untuk admin dan mahasiswa
@login_required
def change_password_mahasiswa(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            # Simpan password baru
            form.save()
            # Perbarui sesi pengguna agar tidak ter-logout
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password berhasil diubah!')

            # Cek role pengguna dan arahkan ke halaman yang sesuai
            if request.user.is_staff:  # Admin
                return redirect('profileadmin')  # Ganti 'admin_dashboard' dengan nama URL untuk dashboard admin
            else:  # Mahasiswa
                return redirect('student_dashboard')  # Ganti 'student_dashboard' dengan nama URL untuk dashboard mahasiswa

        else:
            messages.error(request, 'Terdapat kesalahan. Periksa kembali input Anda.')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'userauths/change_password_mahasiswa.html', {'form': form})



@login_required
def add_student(request):
    if request.method == 'POST':
        form = MahasiswaRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Simpan data form dan profil mahasiswa
            form.save()
            messages.success(request, "Mahasiswa berhasil ditambahkan!")
            return redirect('student_list')  # Ganti dengan URL daftar mahasiswa di admin
        else:
            messages.error(request, "Gagal menambahkan mahasiswa. Periksa kembali data yang dimasukkan.")
            print(f"Form is invalid. Errors: {form.errors}")  # Debugging
    else:
        form = MahasiswaRegistrationForm()

    return render(request, 'admin_coop/add_student.html', {'form': form})