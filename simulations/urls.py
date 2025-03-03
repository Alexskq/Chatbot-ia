from django.urls import path
from . import views

app_name = 'simulations'

urlpatterns = [
    path('create/', views.create_simulation, name='create_simulation'),
] 