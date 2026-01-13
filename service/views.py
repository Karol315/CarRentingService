from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CarSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Car, Rental, UserProfile
from .forms import RentalForm, RegisterForm, LoginForm, ResetPasswordForm



def car_list(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'service/car_list.html', {'cars': cars})

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'service/car_detail.html', {'car': car})


def custom_signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data


            new_user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )

            # 2. Tworzymy profil z adresem
            UserProfile.objects.create(user=new_user, address=data['address'])

            # 3. Pseudo-walidacja na konsolę
            print(f"\n=== NOWA REJESTRACJA ===")
            print(f"Email: {data['email']}")
            print(f"Imię: {data['first_name']} {data['last_name']}")
            print(f"Adres: {data['address']}")
            print(f"========================\n")

            # 4. Logujemy i przekierowujemy
            login(request, new_user, backend='service.backends.EmailBackend')
            return redirect('car_list')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Używamy naszego backendu do sprawdzenia emaila
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('car_list')  # Przekierowanie po sukcesie
            else:
                form.add_error(None, "Błędny e-mail lub hasło.")
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})




def custom_logout(request):
    logout(request)
    return redirect('login')


def custom_password_reset(request):
    sent = False
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Sprawdzamy czy user istnieje
            if User.objects.filter(email=email).exists():
                print(f"\n!!! RESET HASŁA DLA: {email} !!!")
                print(f"LINK RESETUJĄCY: http://127.0.0.1:8000/accounts/login/")  # Tu normalnie byłby link z tokenem
                print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                sent = True
            else:
                form.add_error('email', "Nie znaleziono takiego adresu e-mail.")
    else:
        form = ResetPasswordForm()

    return render(request, 'registration/password_reset.html', {'form': form, 'sent': sent})

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