from .models import Message
from openai import OpenAI
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class ChatbotService:
    def __init__(self, simulation):
        self.simulation = simulation
        self.system_prompt = self._get_system_prompt()
        if not settings.OPENAI_API_KEY:
            raise ValueError("La clé API OpenAI n'est pas configurée")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def _get_system_prompt(self):
        scenario = self.simulation.scenario
        if scenario == 'client_difficile':
            return "Tu es un agent du service client expérimenté, spécialisé dans la gestion des clients difficiles. Tu dois faire preuve de patience, d'empathie et de professionnalisme tout en restant ferme et en trouvant des solutions constructives."
        elif scenario == 'negociation_prix':
            return "Tu es un négociateur commercial expérimenté. Tu dois mener une négociation de prix équilibrée, en défendant les intérêts de l'entreprise tout en cherchant à satisfaire le client."
        elif scenario == 'presentation_produit':
            return "Tu es un expert produit passionné. Tu dois présenter les produits de manière claire et convaincante, en mettant en avant leurs avantages et en répondant précisément aux besoins du client."
        elif scenario == 'gestion_reclamation':
            return "Tu es un spécialiste du service après-vente. Tu dois traiter les réclamations avec sérieux et professionnalisme, en cherchant à comprendre le problème et à proposer des solutions satisfaisantes."
        elif scenario == 'vente_additionnelle':
            return "Tu es un conseiller commercial spécialisé dans la vente additionnelle. Tu dois identifier les opportunités de vente complémentaire pertinentes pour le client, sans être trop insistant."
        # Prompt par défaut si aucun scénario ne correspond
        return "Tu es un assistant virtuel professionnel et serviable, prêt à aider au mieux le client."

    def get_bot_response(self, user_message):
        try:
            # Récupérer l'historique des messages (limité aux 10 derniers)
            conversation_history = Message.objects.filter(simulation=self.simulation).order_by('-timestamp')[:10][::-1]
            
            # Construire le contexte de la conversation pour OpenAI
            messages = []
            messages.append({
                "role": "system",
                "content": self.system_prompt
            })
            
            # Ajouter l'historique des messages
            for msg in conversation_history:
                messages.append({
                    "role": "user" if msg.sender == "user" else "assistant",
                    "content": msg.content
                })
            
            # Ajouter le message actuel
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Appeler l'API OpenAI
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            
            # Extraire et retourner la réponse
            response_message = completion.choices[0].message
            return response_message.content.strip()

        except Exception as e:
            # Log l'erreur en mode silencieux
            logger.debug(f"Erreur OpenAI: {str(e)}")
            return "Une erreur est survenue lors de la communication avec le chatbot." 