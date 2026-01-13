
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Rental, UserProfile
from django import forms
from django.contrib.auth.models import User


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['start_date', 'end_date', 'payment_method', 'insurance_accepted', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}), # <-- dodany widget
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'insurance_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end:
            if start < timezone.now().date():
                raise ValidationError("Data rozpoczęcia nie może być w przeszłości.")
            if end <= start:
                raise ValidationError("Data zakończenia musi być późniejsza niż data rozpoczęcia.")



class RegisterForm(forms.Form):
    # Pola wymagane
    email = forms.EmailField(label="E-mail", widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Imię", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Nazwisko", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_repeat = forms.CharField(label="Powtórz hasło",
                                      widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # Pole opcjonalne
    address = forms.CharField(label="Adres (opcjonalnie)", required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    # Walidacja unikalności e-maila
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ten adres e-mail jest już zajęty.")
        return email

    # Walidacja zgodności haseł
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password_repeat")
        if p1 and p2 and p1 != p2:
            self.add_error('password_repeat', "Hasła muszą być identyczne.")


class LoginForm(forms.Form):
    email = forms.EmailField(label="E-mail", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label="Podaj E-mail", widget=forms.TextInput(attrs={'class': 'form-control'}))