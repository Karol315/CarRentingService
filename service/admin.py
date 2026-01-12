from django.contrib import admin
from .models import Category, Car, Rental

admin.site.register(Category)
admin.site.register(Car)
admin.site.register(Rental)