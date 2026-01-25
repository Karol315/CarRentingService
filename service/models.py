from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nazwa kategorii")
    description = models.TextField(blank=True, verbose_name="Opis")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"


class Car(models.Model):
    GEARBOX_CHOICES = [('manual', 'Manualna'), ('automatic', 'Automatyczna')]

    brand = models.CharField(max_length=100, verbose_name="Marka")
    model = models.CharField(max_length=100, verbose_name="Model")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='cars',
                                 verbose_name="Kategoria")
    production_year = models.PositiveIntegerField(verbose_name="Rok produkcji")
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Cena za dobę (PLN)")
    gearbox = models.CharField(max_length=20, choices=GEARBOX_CHOICES, default='manual', verbose_name="Skrzynia biegów")
    image = models.ImageField(upload_to='cars/', blank=True, null=True, verbose_name="Zdjęcie główne")
    description = models.TextField(verbose_name="Opis wyposażenia")

    def __str__(self):
        return f"{self.brand} {self.model}"

    @property
    def is_fully_available(self):
        for color in self.colors.all():
            if color.is_available:
                return True
        return False

    class Meta:
        verbose_name = "Samochód"
        verbose_name_plural = "Samochody"


class CarColor(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='colors')
    name = models.CharField(max_length=50, verbose_name="Nazwa koloru")
    hex_code = models.CharField(max_length=7, verbose_name="Kod HEX", help_text="np. #FF0000")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Liczba sztuk we flocie")

    def __str__(self):
        return f"{self.name} ({self.car})"

    @property
    def active_rentals_count(self):
        return self.rentals.filter(end_date__gte=timezone.now().date()).count()

    @property
    def available_quantity(self):
        count = self.quantity - self.active_rentals_count
        return max(0, count)

    @property
    def is_available(self):
        return self.available_quantity > 0


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals', verbose_name="Użytkownik")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rentals', verbose_name="Samochód")
    car_color = models.ForeignKey(CarColor, on_delete=models.CASCADE, related_name='rentals',
                                  verbose_name="Wybrany wariant", null=True)

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
            if days < 1: days = 1
            cost = days * self.car.price_per_day
            if self.insurance_accepted: cost += 50
            self.total_cost = cost
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Wypożyczenie"
        verbose_name_plural = "Wypożyczenia"
        ordering = ['-created_at']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Adres zamieszkania")

    def __str__(self): return f"Profil: {self.user.username}"