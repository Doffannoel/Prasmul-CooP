from django.contrib import admin
from .models import MahasiswaProfile, CompanyData , LaporanCOOP 

@admin.register(MahasiswaProfile)
class MahasiswaProfileAdmin(admin.ModelAdmin):
    list_display = ('nim', 'full_name', 'primary_discipline', 'campus_email')  # Hapus 'status'
    search_fields = ('nim', 'full_name', 'campus_email')  # Untuk fitur pencarian

@admin.register(CompanyData)
class CompanyDataAdmin(admin.ModelAdmin):

    list_display = (
        'user_email',
        'company_name', 
        'agency', 
        'start_date', 
        'end_date',
        'comment',
        'supervisor_name', 
        'supervisor_phone', 
        'supervisor_email', 
        'duration_days'
    )
    
    search_fields = ('company_name', 'agency', 'supervisor_name')  
    list_filter = ('start_date', 'end_date') 

    # Menampilkan email pengguna yang mengisi data
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "User Email"  # Nama kolom di admin

    # Membatasi data hanya untuk pengguna yang sedang login (kecuali superuser)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    # Secara otomatis menyimpan pengguna yang sedang login sebagai pengisi data
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Jika data baru
            obj.user = request.user  # Pastikan field user diisi dengan user yang sedang login
        super().save_model(request, obj, form, change)
@admin.register(LaporanCOOP)
class LaporanMagangAdmin(admin.ModelAdmin):
    list_display = ('mahasiswa', 'file_laporan', 'tanggal_upload')  # Kolom yang ditampilkan
    search_fields = ('mahasiswa',)  # Menambahkan fitur pencarian
    list_filter = ('tanggal_upload',)  # Menambahkan filter berdasarkan tanggal
