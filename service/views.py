
from django.shortcuts import render, get_object_or_404, redirect
from .models import Car
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.decorators import login_required
from .forms import RentalForm
from .models import Car, Rental
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CarSerializer

def car_list(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'service/car_list.html', {'cars': cars})

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'service/car_detail.html', {'car': car})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Zaloguj od razu po rejestracji
            return redirect('car_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.car = car
            rental.user = request.user
            rental.save()
            return redirect('my_rentals')  # Przekierowanie do listy rezerwacji
    else:
        form = RentalForm()

    return render(request, 'service/book_car.html', {'form': form, 'car': car})


@login_required
def my_rentals(request):
    # Wymóg: Widok prezentujący zapisane dane
    rentals = Rental.objects.filter(user=request.user)
    return render(request, 'service/my_rentals.html', {'rentals': rentals})


@api_view(['GET'])
def api_car_list(request):
    """Zwraca listę wszystkich dostępnych aut w JSON"""
    cars = Car.objects.filter(is_available=True)
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_car_detail(request, pk):
    """Zwraca szczegóły jednego auta w JSON"""
    car = get_object_or_404(Car, pk=pk)
    serializer = CarSerializer(car)
    return Response(serializer.data)