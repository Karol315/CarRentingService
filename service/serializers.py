from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.ModelSerializer):
    # Dodajemy pole, które jest wyliczane (property w modelu), a nie zapisane w bazie
    is_fully_available = serializers.ReadOnlyField()

    class Meta:
        model = Car
        # Usuwamy 'is_available' z listy, dodajemy 'is_fully_available'
        fields = ['id', 'brand', 'model', 'production_year', 'price_per_day', 'is_fully_available', 'image']