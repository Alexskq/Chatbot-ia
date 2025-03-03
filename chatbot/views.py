from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from simulations.models import Simulation
from .models import Message
from .services import ChatbotService
from django.http import JsonResponse

# Create your views here.

@login_required
def chat_view(request, simulation_id):
    simulation = get_object_or_404(Simulation, pk=simulation_id, user=request.user)
    
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        if user_message:
            # Sauvegarder le message de l'utilisateur
            Message.objects.create(
                simulation=simulation,
                content=user_message,
                sender='user'
            )
            
            # Obtenir la réponse du chatbot
            chatbot = ChatbotService(simulation)
            bot_response = chatbot.get_bot_response(user_message)
            
            # Sauvegarder la réponse du chatbot
            Message.objects.create(
                simulation=simulation,
                content=bot_response,
                sender='bot'
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'bot_response': bot_response
                })
    
    # Récupérer tous les messages de la conversation
    messages = Message.objects.filter(simulation=simulation)
    context = {
        'simulation': simulation,
        'chat_messages': messages  # Renommé pour éviter le conflit avec les messages Django
    }
    return render(request, 'chatbot/chat.html', context)
