from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Message, Simulation
from .services import ChatbotService

# Create your views here.

@login_required
def chat_view(request, simulation_id):
    simulation = get_object_or_404(Simulation, id=simulation_id)
    
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
    chat_messages = Message.objects.filter(simulation=simulation).order_by('timestamp')
    
    return render(request, 'chatbot/chat.html', {
        'simulation': simulation,
        'chat_messages': chat_messages,
    })

def websocket_test_view(request):
    """Vue simple pour tester les WebSockets"""
    return render(request, 'chatbot/websocket_test.html')
