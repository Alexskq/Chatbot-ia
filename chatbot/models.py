from django.db import models
from simulations.models import Simulation

class Message(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    sender = models.CharField(max_length=10, choices=[('user', 'Utilisateur'), ('bot', 'Chatbot')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:50]}..."

    class Meta:
        ordering = ['timestamp']

# Alias pour compatibilité avec le nouveau code
ChatMessage = Message
