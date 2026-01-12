from django import forms
from .models import Rental
from django.core.exceptions import ValidationError
from django.utils import timezone

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