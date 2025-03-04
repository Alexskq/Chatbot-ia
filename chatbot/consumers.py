import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, Simulation
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['simulation_id']
        self.room_group_name = f'chat_{self.room_name}'
        
        logger.info(f"Tentative de connexion WebSocket pour la simulation {self.room_name}")

        # Rejoindre le groupe de la room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        logger.info(f"Connexion WebSocket acceptée pour la simulation {self.room_name}")
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"Déconnexion WebSocket pour la simulation {self.room_name} (code: {close_code})")
        # Quitter le groupe de la room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            
            logger.info(f"Message reçu dans la simulation {self.room_name}: {message[:50]}...")
            
            # Sauvegarder le message de l'utilisateur
            await self.save_message('user', message)
            
            # Envoyer le message de l'utilisateur à tous les clients
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': 'user',
                    'timestamp': datetime.now().strftime('%H:%M')
                }
            )
            
            # Réponse simple pour le débogage
            bot_response = f"Réponse de test à: {message}"
            
            # Sauvegarder la réponse du bot
            await self.save_message('bot', bot_response)
            
            # Envoyer la réponse du bot à tous les clients
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': bot_response,
                    'sender': 'bot',
                    'timestamp': datetime.now().strftime('%H:%M')
                }
            )
        except Exception as e:
            logger.error(f"Erreur dans receive: {str(e)}")
            await self.send(text_data=json.dumps({
                'message': f"Erreur: {str(e)}",
                'sender': 'system',
                'timestamp': datetime.now().strftime('%H:%M')
            }))

    async def chat_message(self, event):
        """
        Gère la réception des messages dans le groupe et les envoie au WebSocket
        """
        try:
            message = event['message']
            sender = event['sender']
            timestamp = event['timestamp']
            
            logger.info(f"Envoi du message au client: {message[:50]}... (sender: {sender})")

            # Envoyer le message au WebSocket
            await self.send(text_data=json.dumps({
                'message': message,
                'sender': sender,
                'timestamp': timestamp
            }))
        except Exception as e:
            logger.error(f"Erreur dans chat_message: {str(e)}")

    @sync_to_async
    def save_message(self, sender, content):
        try:
            simulation = Simulation.objects.get(id=self.room_name)
            Message.objects.create(
                simulation=simulation,
                sender=sender,
                content=content
            )
            logger.info(f"Message sauvegardé: {content[:50]}... (sender: {sender})")
        except Exception as e:
            logger.error(f"Erreur dans save_message: {str(e)}")