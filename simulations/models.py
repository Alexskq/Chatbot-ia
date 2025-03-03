from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Simulation(models.Model):
  SCENARIO_CHOICES = [
    ('client_difficile', 'Client difficile'),
    ('negociation_prix', 'Négociation de prix'),
    ('presentation_produit', 'Présentation de produit'),
    ('gestion_reclamation', 'Gestion de réclamation'),
    ('vente_additionnelle', 'Vente additionnelle'),
  ]
  
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  scenario = models.CharField(max_length=255, choices=SCENARIO_CHOICES, blank=True, null=True)
  status = models.CharField(max_length=255, blank=True, null=True)
  score = models.FloatField(blank=True, null=True)
  start_date = models.DateTimeField(auto_now_add=True)
  end_date = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.user.username} - {self.scenario}"
