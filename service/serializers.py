from rest_framework import serializers
from .models import Car, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CarSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'brand', 'model', 'production_year', 'price_per_day', 'is_available', 'category', 'image']