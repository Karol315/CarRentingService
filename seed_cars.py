import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarRentingServiceProject.settings")
django.setup()

from service.models import Car, Category
from django.core.files import File
from django.conf import settings

categories = {}
for name in ["Sedan", "SUV", "Sport", "Limuzyna"]:
    cat, _ = Category.objects.get_or_create(name=name)
    categories[name] = cat

auta = [
    ("Toyota", "Corolla", "Sedan", 2019, 150, "manual"),
    ("Toyota", "RAV4", "SUV", 2021, 220, "automatic"),
    ("BMW", "3 Series", "Sedan", 2020, 280, "automatic"),
    ("BMW", "X5", "SUV", 2022, 420, "automatic"),
    ("Audi", "A4", "Sedan", 2019, 270, "automatic"),
    ("Audi", "Q7", "SUV", 2021, 450, "automatic"),
    ("Mercedes", "C-Class", "Sedan", 2020, 300, "automatic"),
    ("Mercedes", "GLE", "SUV", 2022, 480, "automatic"),
    ("Ferrari", "488 GTB", "Sport", 2018, 1500, "automatic"),
]

def normalize(text):
    return text.lower().replace(" ", "").replace("-", "")

for marka, model, typ, rok, cena, skrzynia in auta:
    filename = f"{normalize(marka)}_{normalize(typ)}_{normalize(model)}_{rok}.jpg"
    image_path = os.path.join(settings.MEDIA_ROOT, "cars", filename)

    car = Car.objects.create(
        brand=marka,
        model=model,
        category=categories[typ],
        production_year=rok,
        price_per_day=cena,
        gearbox=skrzynia,
        is_available=True,
        description=f"Wyposażenie {marka} {model}"
    )

    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            car.image.save(filename, File(f), save=True)
    else:
        print(f"⚠️ Brak pliku: {image_path}")

print("✅ Samochody dodane")