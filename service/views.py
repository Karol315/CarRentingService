from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CarSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Car, Rental, UserProfile, CarColor, Category
from .forms import RentalForm, RegisterForm, LoginForm, ResetPasswordForm, SetNewPasswordForm
from django.contrib import messages
from django.utils import timezone
from .forms import RentalEditForm

def car_list(request):
    cars = Car.objects.all()

    brand_filter = request.GET.get('brand')
    category_filter = request.GET.get('category')
    color_filter = request.GET.get('color')

    if brand_filter:
        cars = cars.filter(brand__icontains=brand_filter)

    if category_filter:
        cars = cars.filter(category__name__icontains=category_filter)

    if color_filter:
        cars = cars.filter(colors__name__icontains=color_filter).distinct()

    cars_list = list(cars)
    sort_option = request.GET.get('sort', 'price_asc')

    def sort_key(car):
        price = car.price_per_day
        is_unavailable = not car.is_fully_available
        return (is_unavailable, price if sort_option == 'price_asc' else -price)

    cars_list.sort(key=sort_key)

    all_brands = Car.objects.values_list('brand', flat=True).distinct()
    all_categories = Category.objects.values_list('name', flat=True).distinct()
    all_colors = CarColor.objects.values_list('name', flat=True).distinct()

    context = {
        'cars': cars_list,
        'all_brands': all_brands,
        'all_categories': all_categories,
        'all_colors': all_colors,
    }
    return render(request, 'service/car_list.html', context)

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    colors = car.colors.all()
    return render(request, 'service/car_detail.html', {'car': car, 'colors': colors})


@login_required
def my_rentals(request):
    rentals = Rental.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'service/my_rentals.html', {'rentals': rentals})

@login_required
def rental_edit(request, pk):
    rental = get_object_or_404(Rental, pk=pk, user=request.user)
    today = timezone.now().date()
    is_editable = rental.start_date > today

    if request.method == 'POST':
        if not is_editable:
            messages.error(request, "Za późno na edycję.")
            return redirect('my_rentals')

        # 1. ANULOWANIE (Button name='cancel')
        if 'cancel' in request.POST:
            rental.delete()
            messages.info(request, "Rezerwacja została anulowana.")
            return redirect('my_rentals')

        # 2. ZAPIS (Button name='save')
        form = RentalEditForm(request.POST, instance=rental)
        if form.is_valid():
            # Sprawdzamy, czy użytkownik faktycznie coś zmienił
            if form.has_changed():
                form.save()
                messages.success(request, "Zapisano zmiany w rezerwacji.")
            else:
                # Jeśli nic nie zmienił, po prostu wracamy bez krzyczenia
                return redirect('my_rentals')

            return redirect('my_rentals')
    else:
        form = RentalEditForm(instance=rental)

    return render(request, 'service/rental_edit.html', {
        'rental': rental,
        'form': form,
        'is_editable': is_editable
    })
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
            UserProfile.objects.create(user=new_user, address=data['address'])
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
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('car_list')
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
            if User.objects.filter(email=email).exists():
                link = f"http://127.0.0.1:8000/reset-password-confirm/{email}/"
                print(f"\nRESET HASŁA: {link}\n")
                sent = True
            else:
                form.add_error('email', "Nie znaleziono takiego adresu e-mail.")
    else:
        form = ResetPasswordForm()
    return render(request, 'registration/password_reset.html', {'form': form, 'sent': sent})


def custom_password_reset_confirm(request, email):
    user = get_object_or_404(User, email=email)
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = SetNewPasswordForm()
    return render(request, 'registration/password_set_new.html', {'form': form, 'email': email})


@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    if request.method == 'POST':
        form = RentalForm(request.POST, car_id=car.id)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.car = car
            rental.user = request.user
            rental.save()
            return redirect('my_rentals')
    else:
        form = RentalForm(car_id=car.id)

    return render(request, 'service/book_car.html', {'form': form, 'car': car})


@login_required
def my_rentals(request):
    rentals = Rental.objects.filter(user=request.user)
    return render(request, 'service/my_rentals.html', {'rentals': rentals})


@api_view(['GET'])
def api_car_list(request):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    serializer = CarSerializer(car)
    return Response(serializer.data)