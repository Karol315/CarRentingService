from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.ModelSerializer):
    is_fully_available = serializers.ReadOnlyField()

    class Meta:
        model = Car
        fields = ['id', 'brand', 'model', 'production_year', 'price_per_day', 'is_fully_available', 'image']