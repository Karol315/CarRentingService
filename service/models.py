from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nazwa kategorii")
    description = models.TextField(blank=True, verbose_name="Opis")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"


class Car(models.Model):
    GEARBOX_CHOICES = [
        ('manual', 'Manualna'),
        ('automatic', 'Automatyczna'),
    ]

    brand = models.CharField(max_length=100, verbose_name="Marka")
    model = models.CharField(max_length=100, verbose_name="Model")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='cars',
                                 verbose_name="Kategoria")
    production_year = models.PositiveIntegerField(verbose_name="Rok produkcji")
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Cena za dobę (PLN)")
    gearbox = models.CharField(max_length=20, choices=GEARBOX_CHOICES, default='manual', verbose_name="Skrzynia biegów")
    is_available = models.BooleanField(default=True, verbose_name="Dostępny")
    image = models.ImageField(upload_to='cars/', blank=True, null=True, verbose_name="Zdjęcie")
    description = models.TextField(verbose_name="Opis wyposażenia")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.production_year})"

    class Meta:
        verbose_name = "Samochód"
        verbose_name_plural = "Samochody"


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals', verbose_name="Użytkownik")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rentals', verbose_name="Samochód")
    start_date = models.DateField(verbose_name="Data rozpoczęcia")
    end_date = models.DateField(verbose_name="Data zakończenia")
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True,
                                     verbose_name="Koszt całkowity")
    created_at = models.DateTimeField(auto_now_add=True)
    insurance_accepted = models.BooleanField(default=False, verbose_name="Dodatkowe ubezpieczenie (+50 PLN)")
    notes = models.TextField(blank=True, verbose_name="Uwagi do rezerwacji")

    PAYMENT_CHOICES = [
        ('card', 'Karta kredytowa/debetowa'),
        ('transfer', 'Przelew tradycyjny'),
        ('blik', 'BLIK'),
        ('cash', 'Gotówka przy odbiorze'),
    ]

    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='card',
                                      verbose_name="Metoda płatności")

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date and self.car:
            days = (self.end_date - self.start_date).days
            if days < 1:
                days = 1
            cost = days * self.car.price_per_day
            # Doliczamy 50 zł jeśli wybrano ubezpieczenie
            if self.insurance_accepted:
                cost += 50
            self.total_cost = cost
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rezerwacja: {self.car} przez {self.user}"

    class Meta:
        verbose_name = "Wypożyczenie"
        verbose_name_plural = "Wypożyczenia"
        ordering = ['-created_at']



