# Generated by Django 5.1.6 on 2025-03-03 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulations', '0002_alter_simulation_scenario_alter_simulation_score_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='scenario',
            field=models.CharField(blank=True, choices=[('client_difficile', 'Client difficile'), ('negociation_prix', 'Négociation de prix'), ('presentation_produit', 'Présentation de produit'), ('gestion_reclamation', 'Gestion de réclamation'), ('vente_additionnelle', 'Vente additionnelle')], max_length=255, null=True),
        ),
    ]
