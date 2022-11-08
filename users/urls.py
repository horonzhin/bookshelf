from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Registration.as_view(), name='register'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('logout/', views.logout, name='logout'),
]