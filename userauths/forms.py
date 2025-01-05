from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from mahasiswa_coop.models import MahasiswaProfile
from userauths.models import CustomUser
from django.contrib.auth import get_user_model

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "input-field",
                "placeholder": "Email",
                "autofocus": True,  # Fokus otomatis di kolom email
            }
        ),
        label="Email",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input-field",
                "placeholder": "Password",
            }
        ),
        label="Password",
    )

    def clean(self):
        # Validasi tambahan jika diperlukan
        cleaned_data = super().clean()
        email = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not email or not password:
            raise forms.ValidationError("Email dan password wajib diisi.")

        return cleaned_data

User = get_user_model()

class MahasiswaRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = MahasiswaProfile
        fields = ['nim', 'full_name', 'birth_date', 'study_mode', 'primary_discipline', 'mobile_phone', 'campus_email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        # Validasi password dan konfirmasi password
        if password != confirm_password:
            raise forms.ValidationError("Password dan konfirmasi password tidak cocok.")
        
        # Validasi email kampus
        email_kampus = cleaned_data.get('campus_email')
        nim = cleaned_data.get('nim')
        if not email_kampus.endswith('@student.prasetiyamulya.ac.id') or not email_kampus.startswith(f"{nim}"):
            raise forms.ValidationError("Email kampus harus berupa NIM@student.prasetiyamulya.ac.id")

        return cleaned_data

    def save(self, commit=True):
        # Simpan CustomUser dan profil mahasiswa
        user = User.objects.create_user(
            email=self.cleaned_data['campus_email'],
            password=self.cleaned_data['password'],  # Set password dari form
            is_student=True,
            is_admin_coop=False
        )

        # Setelah user dibuat, buat profil mahasiswa
        mahasiswa_profile = MahasiswaProfile.objects.create(
            user=user,
            nim=self.cleaned_data['nim'],
            full_name=self.cleaned_data['full_name'],
            birth_date=self.cleaned_data['birth_date'],
            study_mode=self.cleaned_data['study_mode'],
            primary_discipline=self.cleaned_data['primary_discipline'],
            mobile_phone=self.cleaned_data['mobile_phone'],
            campus_email=self.cleaned_data['campus_email']
        )

        return mahasiswa_profile
    
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Password Lama'
        }),
        label="Password Lama"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Password Baru'
        }),
        label="Password Baru"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Konfirmasi'
        }),
        label="Konfirmasi"
    )

