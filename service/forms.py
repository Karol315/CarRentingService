from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Rental, UserProfile, CarColor


class RentalForm(forms.ModelForm):
    car_color = forms.ModelChoiceField(
        queryset=CarColor.objects.none(),
        label="Wybierz wariant",
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="-- Wybierz kolor --"
    )

    class Meta:
        model = Rental
        fields = ['start_date', 'end_date', 'car_color', 'payment_method', 'insurance_accepted', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'insurance_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        car_id = kwargs.pop('car_id', None)
        super().__init__(*args, **kwargs)

        if car_id:
            colors = CarColor.objects.filter(car_id=car_id)
            self.fields['car_color'].queryset = colors

            self.fields['car_color'].label_from_instance = lambda \
                    obj: f"{obj.name} (Wolne: {obj.available_quantity} szt.)"

            if not colors.exists():
                self.fields['car_color'].widget.attrs['disabled'] = True
                self.fields['car_color'].help_text = "Brak skonfigurowanych kolorów dla tego auta w bazie."

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")
        chosen_color = cleaned_data.get("car_color")

        if start and end:
            if start < timezone.now().date():
                raise ValidationError("Data rozpoczęcia nie może być w przeszłości.")
            if end <= start:
                raise ValidationError("Data zwrotu musi być późniejsza niż odbioru.")

        if chosen_color:
            if not chosen_color.is_available:
                raise ValidationError(f"Wariant {chosen_color.name} jest niedostępny.")

class RentalEditForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['notes']
        labels = {
            'notes': 'Uwagi do rezerwacji'
        }
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class RegisterForm(forms.Form):
    email = forms.EmailField(label="E-mail", widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Imię", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Nazwisko", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_repeat = forms.CharField(label="Powtórz hasło",
                                      widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label="Adres (opcjonalnie)", required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ten adres e-mail jest już zajęty.")
        return email

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


class SetNewPasswordForm(forms.Form):
    password = forms.CharField(label="Nowe hasło", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_repeat = forms.CharField(label="Powtórz hasło",
                                      widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password_repeat")
        if p1 and p2 and p1 != p2:
            self.add_error('password_repeat', "Hasła muszą być identyczne.")