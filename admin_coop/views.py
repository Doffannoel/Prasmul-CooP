from urllib.parse import quote, urlencode
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from mahasiswa_coop.models import MahasiswaProfile, CompanyData, LaporanCOOP
from .forms import AdminProfileForm, CompanyDataForm, StudentFilterForm  
from .forms import MahasiswaProfileForm  # Assuming you have a form for adding students
from .models import AdminProfile
from django.contrib import messages
from django.db.models.functions import TruncMonth
from django.db.models import Count
from datetime import datetime

@login_required
def student_list(request):
    if not request.user.is_admin_coop:
        return HttpResponseForbidden("You do not have permission to access this page.")

    form = StudentFilterForm(request.GET or None)
    students = MahasiswaProfile.objects.all()

    # Cek jika form valid, gabungkan semua filter dalam satu langkah
    if form.is_valid():
        filters = {}

        nim = form.cleaned_data.get('nim')
        full_name = form.cleaned_data.get('full_name')
        campus_email = form.cleaned_data.get('campus_email')
        primary_discipline = form.cleaned_data.get('primary_discipline')
        company_status = form.cleaned_data.get('company_status')

        if nim:
            filters['nim__icontains'] = nim
        if full_name:
            filters['full_name__icontains'] = full_name
        if campus_email:
            filters['campus_email__icontains'] = campus_email
        if primary_discipline and primary_discipline != 'All':
            filters['primary_discipline'] = primary_discipline

        if company_status == 'submitted':
            filters['company_data__isnull'] = False  # Mahasiswa yang sudah mengisi form perusahaan
        elif company_status == 'not_submitted':
            filters['company_data__isnull'] = True   # Mahasiswa yang belum mengisi form perusahaan

        # Terapkan semua filter sekaligus
        students = students.filter(**filters).distinct()

    return render(request, 'admin_coop/studentlist.html', {'students': students, 'form': form})


@login_required
def admin_profile(request):
    # Ambil profil admin berdasarkan user yang login
    profile = get_object_or_404(AdminProfile, user=request.user)

    if request.method == 'POST':
        # Proses form jika data dikirim
        form = AdminProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('admin_profile')  # Redirect ke halaman profil setelah menyimpan
        else:
            print(form.errors)
            messages.error(request, "Failed to update profile. Please correct the errors below.")
    else:
        # Form untuk pengeditan (GET request)
        form = AdminProfileForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'admin_coop/profileadmin.html', context)



def student_profile(request, nim):
    # Ambil profil mahasiswa berdasarkan NIM
    student = get_object_or_404(MahasiswaProfile, nim=nim)
    
    # Ambil data perusahaan yang terkait dengan mahasiswa
    company_data = CompanyData.objects.filter(user=student.user)
    
    # Ambil laporan yang sudah diupload oleh mahasiswa ini
    laporan = LaporanCOOP.objects.filter(mahasiswa=student)

    # Form untuk MahasiswaProfile
    if request.method == 'POST' and 'save_student' in request.POST:
        form = MahasiswaProfileForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            old_nim = student.nim  # Simpan NIM sebelum diubah
            student.save()  # Simpan perubahan ke database
            new_nim = student.nim  # Dapatkan NIM baru

            if old_nim != new_nim:
                messages.success(request, "NIM berhasil diubah. Anda diarahkan ke daftar mahasiswa.")
                return redirect('student_list')
            else:
                messages.success(request, "Profil mahasiswa berhasil diperbarui.")
                return redirect('student_profile', nim=new_nim)
    elif 'delete_student' in request.POST:
        student.delete()
        return redirect('student_list')
    else:
        form = MahasiswaProfileForm(instance=student)

    context = {
        'student': student,
        'form': form,
        'company_data': company_data,  # Kirimkan data perusahaan ke template
        'laporan': laporan,  # Kirimkan laporan ke template
    }
    return render(request, 'admin_coop/student_detail.html', context)

@login_required
def company_data(request, nim):
    # Ambil profil mahasiswa
    student = get_object_or_404(MahasiswaProfile, nim=nim)
    
    # Ambil data perusahaan yang terkait dengan mahasiswa
    company_data = CompanyData.objects.filter(user=student.user)

    # Menangani penambahan atau pengeditan data perusahaan
    if request.method == 'POST':
        if 'edit_company' in request.POST:
            # Mengedit data perusahaan yang ada
            company_id = request.POST.get('company_id')
            company = get_object_or_404(CompanyData, id=company_id)
            company_form = CompanyDataForm(request.POST, instance=company)
            if company_form.is_valid():
                company_form.save()
                messages.success(request, "Data perusahaan berhasil diperbarui.")
                return redirect('company_data', nim=student.nim)
        
        elif 'delete_company' in request.POST:
            # Menghapus data perusahaan
            company_id = request.POST.get('company_id')
            company = get_object_or_404(CompanyData, id=company_id)
            company.delete()
            messages.success(request, "Data perusahaan berhasil dihapus.")
            return redirect('company_data', nim=student.nim)
    else:
        company_form = CompanyDataForm()

    context = {
        'student': student,
        'company_data': company_data,
        'company_form': company_form,  # Menampilkan form perusahaan (untuk tambah/edit)
    }
    return render(request, 'admin_coop/student_detail.html', context)


@login_required
def grafik_view(request):
    # Rentang bulan yang diinginkan
    start_date = datetime(2024, 9, 1)  # September 2024
    end_date = datetime(2025, 8, 31)  # Agustus 2025

    # Ambil data jumlah mahasiswa yang mendaftar berdasarkan bulan
    monthly_signups = CompanyData.objects.annotate(
        month=TruncMonth('start_date')
    ).values('month').annotate(
        student_count=Count('id')
    ).filter(month__gte=start_date, month__lte=end_date).order_by('month')

    # List bulan-bulan dari September 2024 hingga Agustus 2025
    months = []
    current_month = start_date
    while current_month <= end_date:
        months.append(current_month.strftime('%b %Y'))  # Format bulan dan tahun (contoh: Jan 2024)
        current_month = current_month.replace(month=current_month.month + 1 if current_month.month < 12 else 1,
                                                year=current_month.year if current_month.month < 12 else current_month.year + 1)

    # Siapkan data untuk grafik (Isi data untuk bulan yang tidak ada)
    monthly_data = {month: 0 for month in months}
    for signup in monthly_signups:
        month_str = signup['month'].strftime('%b %Y')
        monthly_data[month_str] = signup['student_count']

    # Hitung jumlah mahasiswa yang sudah dan belum mengisi form perusahaan
    total_students = MahasiswaProfile.objects.count()
    # Menghitung jumlah mahasiswa yang sudah mengisi form secara unik
    students_with_company_data = MahasiswaProfile.objects.filter(company_data__isnull=False).distinct().count()
    students_without_company_data = total_students - students_with_company_data

    # Kirim data ke template
    context = {
        'months': months,
        'student_counts': [monthly_data[month] for month in months],
        'students_with_company_data': students_with_company_data,
        'students_without_company_data': students_without_company_data,
    }
    return render(request, 'admin_coop/grafik_page.html', context)

@login_required
def add_student(request):
    if request.method == 'POST':
        form = MahasiswaProfileForm(request.POST)
        if form.is_valid():
            # Tambahkan logika untuk menghubungkan dengan user
            mahasiswa = form.save(commit=False)
            
            # Pastikan Anda membuat atau mengaitkan dengan CustomUser
            # Contoh:
            try:
                user = CustomUser.objects.create_user(
                    username=form.cleaned_data['nim'],  # NIM sebagai username
                    email=form.cleaned_data['campus_email']
                )
                mahasiswa.user = user
                mahasiswa.save()
            except Exception as e:
                messages.error(request, f"Error creating user: {str(e)}")
                return render(request, 'admin_coop/add_student.html', {'form': form})

            messages.success(request, "Student successfully added.")
            return redirect('student_list')
        else:
            messages.error(request, "Failed to add student. Please check the form.")
    else:
        form = MahasiswaProfileForm()
    
    context = {
        'form': form,
    }
    return render(request, 'admin_coop/add_student.html', context)

def send_supervisor_email(request, company_id):
    # Ambil data perusahaan berdasarkan ID
    company = get_object_or_404(CompanyData, id=company_id)

    # Ambil nama supervisor, email, dan informasi mahasiswa
    supervisor_name = company.supervisor_name
    supervisor_email = company.supervisor_email
    mahasiswa_profile = company.mahasiswa_profile
    mahasiswa_name = mahasiswa_profile.full_name

    # Ambil nama admin dari AdminProfile yang terkait dengan user yang sedang login
    admin_profile = get_object_or_404(AdminProfile, user=request.user)
    admin_name = admin_profile.full_name

    # Template body email (Plain text)
    email_subject = f"Permintaan Pengisian Form Evaluasi Penilaian Mahasiswa"
    email_body = f"""Kepada Yang Terhormat, Bapak/Ibu {supervisor_name}.

Perkenalkan, saya {admin_name} dari pihak Admin Program Coop Prasetiya Mulya, izin meminta Bapak/Ibu untuk bisa mengisi form laporan kinerja magang mahasiswa kami, yang bernama {mahasiswa_name}.

Formulir ini penting bagi kami untuk mendapatkan feedback yang berharga mengenai perkembangan mahasiswa selama menjalani program magang, guna meningkatkan kualitas program dan mendukung kemajuan mahasiswa kami

Untuk link formulir kinerja magang, dapat diklik di link berikut:
https://docs.google.com/forms/d/e/1FAIpQLScEib3x9AhbHs5ftdXytImR_PxTDBZue24nwrt23Ub-ymNOZA/viewform?usp=header
    
Jika ada pertanyaan atau hal lain yang perlu didiskusikan, jangan ragu untuk menghubungi kami. Terima kasih banyak atas kerjasama dan perhatian Bapak/Ibu. Kami sangat mengapresiasi dukungan Bapak/Ibu terhadap mahasiswa kami.

Hormat Kami,  
{ admin_name }  
Admin Program Co-op  
Universitas Prasetiya Mulya
"""
# {company.google_form_link}
    # Encode subject dan body agar aman di URL
    email_subject_encoded = quote(email_subject)
    email_body_encoded = quote(email_body)

    # URL mailto dengan email, subject, dan body yang sudah diencode
    mailto_url = f"mailto:{supervisor_email}?subject={email_subject_encoded}&body={email_body_encoded}"

    # Halaman HTML dengan redirect otomatis ke mailto URL
    html_content = f"""
    <html>
        <body>
            <script type="text/javascript">
                window.location.href = "{mailto_url}";
            </script>
            <p>Jika email tidak terbuka otomatis, silakan klik <a href="{mailto_url}">disini</a>.</p>
        </body>
    </html>
    """

    return HttpResponse(html_content)