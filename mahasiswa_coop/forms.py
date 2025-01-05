from django import forms
from .models import CompanyData , LaporanCOOP

class CompanyDataForm(forms.ModelForm):
    class Meta:
        model = CompanyData
        fields = ['company_name', 'agency', 'start_date', 'end_date', 'comment', 
                  'supervisor_name', 'supervisor_phone', 'supervisor_email', 'duration_days']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'required': 'required'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'required': 'required'}),
            'company_name': forms.TextInput(attrs={'required': 'required'}),
            'agency': forms.TextInput(attrs={'required': 'required'}),
            'supervisor_name': forms.TextInput(attrs={'required': 'required'}),
            'supervisor_phone': forms.TextInput(attrs={'required': 'required'}),
            'supervisor_email': forms.EmailInput(attrs={'required': 'required'}),
            'duration_days': forms.NumberInput(attrs={'required': 'required'}),
        }
class LaporanCOOPForm(forms.ModelForm):
    class Meta:
        model = LaporanCOOP
        fields = ['file_laporan']  

