from django.contrib import admin
from .models import Car, Category, Rental, UserProfile, CarColor

# Pozwala dodawać kolory bezpośrednio w edycji Samochodu
class CarColorInline(admin.TabularInline):
    model = CarColor
    extra = 1

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'production_year', 'price_per_day', 'is_fully_available')
    list_filter = ('brand', 'category')
    search_fields = ('brand', 'model')
    inlines = [CarColorInline] # <-- Dodajemy inline

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'car_color', 'start_date', 'end_date', 'total_cost')
    list_filter = ('created_at',)

admin.site.register(Category)
admin.site.register(UserProfile)
# CarColor nie musi być rejestrowany oddzielnie, bo jest w Car, ale można:
admin.site.register(CarColor)