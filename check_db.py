import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarRentingServiceProject.settings')
django.setup()

from service.models import Car, CarColor

print("--- DIAGNOSTYKA BAZY DANYCH ---")
cars = Car.objects.all()
if not cars.exists():
    print("BŁĄD: Brak samochodów w bazie (Tabela Car pusta).")
else:
    print(f"✅ Znaleziono {cars.count()} samochodów.")
    for car in cars:
        colors = CarColor.objects.filter(car=car)
        print(f"\nAuto: {car.brand} {car.model}")
        if not colors.exists():
            print("   ❌ BRAK KOLORÓW! (To dlatego lista jest pusta)")
        else:
            for c in colors:
                print(f"   - Kolor: {c.name}, Ilość całkowita: {c.quantity}, Dostępne: {c.available_quantity}")

print("\n-------------------------------")