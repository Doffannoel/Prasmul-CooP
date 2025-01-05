from django import forms
from admin_coop.models import AdminProfile
from mahasiswa_coop.models import MahasiswaProfile, CompanyData

class MahasiswaProfileForm(forms.ModelForm):
    class Meta:
        model = MahasiswaProfile
        fields = ['nim', 'full_name', 'birth_date', 'study_mode', 'primary_discipline', 'mobile_phone', 'campus_email']

class CompanyDataForm(forms.ModelForm):
    class Meta:
        model = CompanyData
        fields = ['company_name', 'agency', 'start_date', 'end_date', 'comment', 'supervisor_name', 'supervisor_phone', 'supervisor_email', 'duration_days']

class StudentFilterForm(forms.Form):
    nim = forms.CharField(required=False, label="NIM", widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(required=False, label="Nama Lengkap", widget=forms.TextInput(attrs={'class': 'form-control'}))
    campus_email = forms.EmailField(required=False, label="Email Kampus", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    company_status_choices = [
        ('', 'All'),
        ('submitted', 'Sudah Mengisi'),
        ('not_submitted', 'Belum Mengisi'),
    ]

    company_status = forms.ChoiceField(choices=company_status_choices, required=False, label='Form Perusahaan', widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(StudentFilterForm, self).__init__(*args, **kwargs)
        primary_discipline_choices = MahasiswaProfile.objects.values_list('primary_discipline', flat=True).distinct()
        choices = [('', 'All')] + [(choice, choice) for choice in primary_discipline_choices if choice]
        self.fields['primary_discipline'] = forms.ChoiceField(
            choices=choices,
            required=False,
            label='Discipline',
            widget=forms.Select(attrs={'class': 'form-control'})
        )



class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = ['full_name', 'gender', 'staff_code', ]
        widgets = {
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female')]),
        }