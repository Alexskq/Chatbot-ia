from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('simulation/<int:simulation_id>/', views.chat_view, name='chat'),
] 