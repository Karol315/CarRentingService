from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('signup/', views.signup, name='signup'),

    # Nowe:
    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('my-rentals/', views.my_rentals, name='my_rentals'),






    # API Endpoints
    path('api/cars/', views.api_car_list, name='api_car_list'),
    path('api/cars/<int:pk>/', views.api_car_detail, name='api_car_detail'),
]