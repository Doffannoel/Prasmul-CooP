from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required  # Tambahkan ini
from django.contrib import messages
from .forms import CompanyDataForm, LaporanCOOPForm
from .models import CompanyData , LaporanCOOP
from .models import MahasiswaProfile 
from mahasiswa_coop.models import MahasiswaProfile
from .forms import CompanyDataForm
import logging
from django.conf import settings
from django.utils import timezone
import os
from django.utils import timezone

@login_required
def student_dashboard(request):
    profile = MahasiswaProfile.objects.filter(user=request.user).first()
    
    if not profile:
        messages.warning(request, "Profil Anda belum lengkap. Silakan hubungi admin.", extra_tags='dashboard')
    
    company_data = CompanyData.objects.filter(user=request.user)
    if company_data.exists():
        messages.warning(request, "Tidak ada data perusahaan yang terdaftar.", extra_tags='dashboard')
    
    last_login = request.user.last_login
    if last_login:
        last_login = timezone.localtime(last_login)

    return render(request, 'mahasiswa_coop/dashboard.html', {
        'profile': profile,
        'company_data': company_data,
        'last_login': last_login
    })


@login_required
def company_form(request):
    success = False 
    if request.method == 'POST':
        form = CompanyDataForm(request.POST)
        if form.is_valid():
            company_data = form.save(commit=False)  
            company_data.user = request.user  
            company_data.save()  
            messages.success(request, "Data berhasil dikirim!") 
            success = True  
        else:
            messages.error(request, 'Form tidak valid. Periksa kembali data yang Anda masukkan.')
    else:
        form = CompanyDataForm()
    return render(request, 'mahasiswa_coop/company_form.html', {'form': form, 'success': success})

@login_required
def mahasiswa_profile_view(request):
    # Ambil profil mahasiswa berdasarkan user yang login
    profile = get_object_or_404(MahasiswaProfile, user=request.user)

    context = {
        'profile': profile
    }
    return render(request, 'profile.html', context)

@login_required
def upload_laporan(request):
    try:
        mahasiswa = MahasiswaProfile.objects.get(user=request.user)
        laporan_terakhir = LaporanCOOP.objects.filter(mahasiswa=mahasiswa).order_by('-tanggal_upload').first()
    except MahasiswaProfile.DoesNotExist:
        mahasiswa = None
        laporan_terakhir = None

    if request.method == 'POST':
        form = LaporanCOOPForm(request.POST, request.FILES)
        if form.is_valid():
            laporan = form.save(commit=False)
            if mahasiswa:
                laporan.mahasiswa = mahasiswa
                laporan.judul_laporan = laporan.file_laporan.name.split('/')[-1]
                laporan.save()
                messages.success(request, f"Laporan '{laporan.judul_laporan}' berhasil diunggah.")
                return redirect('upload_laporan')
            else:
                messages.error(request, 'Profil mahasiswa tidak ditemukan.')
        else:
            messages.error(request, 'Terjadi kesalahan. Pastikan semua data sudah diisi dengan benar.')
    else:
        form = LaporanCOOPForm()

    return render(request, 'mahasiswa_coop/upload_laporan.html', {
        'form': form,
        'laporan_terakhir': laporan_terakhir  # Mengirim laporan terakhir ke template
    })






