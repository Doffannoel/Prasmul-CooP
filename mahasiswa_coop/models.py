from django.db import models
from userauths.models import CustomUser
from django.conf import settings

class MahasiswaProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='mahasiswa_profile')
    nim = models.CharField(max_length=20, unique=True)  # Nomor Induk Mahasiswa
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    study_mode = models.CharField(
        max_length=10,
        choices=[('Fulltime', 'Fulltime'), ('Parttime', 'Parttime')]
    )
    primary_discipline = models.CharField(
        max_length=50,  # Membatasi panjang input menjadi 50 karakter
        choices=[
            ('Business Mathematics', 'Business Mathematics'),
            ('School of Applied STEM', 'School of Applied STEM')
        ],
        default=""  # Nilai default
    )
    mobile_phone = models.CharField(max_length=15)
    campus_email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.nim

    def save(self, *args, **kwargs):
        # Pastikan email kampus sesuai format tertentu, jika ada
        if not self.campus_email.endswith('@student.prasetiyamulya.ac.id'):
            raise ValueError("Campus email must end with '@student.prasetiyamulya.ac.id'")
        super().save(*args, **kwargs)

class CompanyData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    agency = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    comment = models.TextField(blank=True)
    supervisor_name = models.CharField(max_length=100, null=True, blank=True)
    supervisor_phone = models.CharField(max_length=15, null=True, blank=True)
    supervisor_email = models.EmailField(max_length=100, null=True, blank=True)
    duration_days = models.IntegerField(null=True, blank=True)

    mahasiswa_profile = models.ForeignKey(MahasiswaProfile, on_delete=models.CASCADE, related_name='company_data', default=1)
    google_form_link = models.URLField(max_length=500, blank=True, null=True)  # Menyimpan link Google Form

    def __str__(self):
        return f"{self.company_name}"  
    
    def is_filled(self):
        # Menentukan apakah semua kolom penting sudah terisi
        return all([self.company_name, self.agency, self.start_date, self.end_date])

class LaporanCOOP(models.Model):
    mahasiswa = models.ForeignKey(
        MahasiswaProfile, 
        on_delete=models.CASCADE, 
        related_name='laporan_coop',
        null=True,  # Izinkan nilai NULL
        blank=True  # Izinkan kosong di form
    )
    file_laporan = models.FileField(upload_to='laporan_coop/', null=True, blank=True)
    tanggal_upload = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    judul_laporan = models.CharField(max_length=255, null=True, blank=True)  # Menyimpan judul laporan

    def _str_(self):
        return f"{self.judul_laporan} oleh {self.mahasiswa.full_name if self.mahasiswa else 'Tidak ada mahasiswa'}"

    

