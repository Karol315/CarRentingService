import os
import django

# Konfiguracja środowiska Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarRentingServiceProject.settings')
django.setup()

from service.models import Category, Car, CarColor


def run():
    print("--- GENEROWANIE BAZY DANYCH ---")

    # 1. KATEGORIE
    cat_suv, _ = Category.objects.get_or_create(name="SUV", defaults={'description': "Rodzinne i terenowe"})
    cat_sedan, _ = Category.objects.get_or_create(name="Sedan", defaults={'description': "Limuzyny na trasy"})
    cat_sport, _ = Category.objects.get_or_create(name="Sport", defaults={'description': "Szybkie i dynamiczne"})

    # 2. DEFINICJE KOLORÓW (Podstawowa paleta)
    COLORS_PALETTE = {
        "Czarny": "#000000",
        "Biały": "#FFFFFF",
        "Granatowy": "#000080",
        "Czerwony": "#FF0000",
        "Srebrny": "#C0C0C0",
        "Szary": "#808080",  # +1
        "Niebieski": "#0000FF"  # +2
    }

    # 3. DANE SAMOCHODÓW
    cars_data = [
        {
            "brand": "Audi", "model": "A4", "year": 2019, "price": 199.00,
            "category": cat_sedan, "img_name": "audi_sedan_a4_2019.jpg",
            "desc": "Komfortowa limuzyna.",
            "variants": [("Czarny", 2), ("Srebrny", 1)]  # (Nazwa z palety, Ilość sztuk)
        },
        {
            "brand": "Audi", "model": "Q7", "year": 2021, "price": 450.00,
            "category": cat_suv, "img_name": "audi_suv_q7_2021.jpg",
            "desc": "Luksusowy SUV.",
            "variants": [("Biały", 1), ("Szary", 1)]
        },
        {
            "brand": "BMW", "model": "Seria 3", "year": 2020, "price": 220.00,
            "category": cat_sedan, "img_name": "bmw_sedan_3series_2020.jpg",
            "desc": "Sportowy sedan.",
            "variants": [("Niebieski", 2), ("Czarny", 2)]
        },
        {
            "brand": "BMW", "model": "X5", "year": 2022, "price": 500.00,
            "category": cat_suv, "img_name": "bmw_suv_x5_2022.jpg",
            "desc": "Dominujący SUV.",
            "variants": [("Czarny", 1), ("Biały", 1)]
        },
        {
            "brand": "Ferrari", "model": "488 GTB", "year": 2018, "price": 1200.00,
            "category": cat_sport, "img_name": "ferrari_sport_488gtb_2018.jpg",
            "desc": "Włoska legenda. V8 turbo.",
            "variants": [("Czerwony", 1), ("Żółty", 0)]
            # Żółty niedostępny (brak w palecie HEX u góry, więc dodam ręcznie niżej)
        },
        {
            "brand": "Mercedes", "model": "C-Class", "year": 2020, "price": 210.00,
            "category": cat_sedan, "img_name": "mercedes_sedan_cclass_2020.jpg",
            "desc": "Elegancja i styl.",
            "variants": [("Srebrny", 2), ("Granatowy", 1)]
        },
        {
            "brand": "Toyota", "model": "Corolla", "year": 2019, "price": 120.00,
            "category": cat_sedan, "img_name": "toyota_sedan_corolla_2019.jpg",
            "desc": "Niezawodna hybryda.",
            "variants": [("Biały", 3), ("Srebrny", 2)]
        },
        {
            "brand": "Toyota", "model": "RAV4", "year": 2021, "price": 180.00,
            "category": cat_suv, "img_name": "toyota_suv_rav4_2021.jpg",
            "desc": "Wszechstronny SUV.",
            "variants": [("Niebieski", 2), ("Szary", 1)]
        },
    ]

    for item in cars_data:
        car, created = Car.objects.get_or_create(
            brand=item["brand"], model=item["model"], production_year=item["year"],
            defaults={
                "category": item["category"], "price_per_day": item["price"],
                "description": item["desc"], "gearbox": "automatic"
            }
        )
        if created and item['img_name']:
            car.image.name = f"cars/{item['img_name']}"
            car.save()
            print(f"Dodano auto: {car}")

        # Warianty
        for color_name, qty in item["variants"]:
            # Pobieramy HEX z palety, jeśli nie ma (np. żółty Ferrari) dajemy domyślny
            hex_code = COLORS_PALETTE.get(color_name, "#FFFF00")

            CarColor.objects.get_or_create(
                car=car, name=color_name,
                defaults={"hex_code": hex_code, "quantity": qty}
            )

    print("\n--- BAZA GOTOWA! ---")


if __name__ == "__main__":
    run()