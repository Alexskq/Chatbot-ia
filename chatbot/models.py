from django.db import models
from simulations.models import Simulation

class Message(models.Model):
    SENDER_CHOICES = [
        ('user', 'Utilisateur'),
        ('bot', 'Chatbot'),
    ]

    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.get_sender_display()} - {self.timestamp.strftime('%H:%M:%S')}"
