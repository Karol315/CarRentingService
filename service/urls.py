from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('my-rentals/', views.my_rentals, name='my_rentals'),
    path('rentals/edit/<int:pk>/', views.rental_edit, name='rental_edit'),
    path('signup/', views.custom_signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('reset-password/', views.custom_password_reset, name='password_reset'),
    path('reset-password-confirm/<str:email>/', views.custom_password_reset_confirm, name='password_reset_confirm'),

    # API
    path('api/cars/', views.api_car_list, name='api_car_list'),
    path('api/cars/<int:pk>/', views.api_car_detail, name='api_car_detail'),
]