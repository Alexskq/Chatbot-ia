from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Simulation
from django.contrib import messages

# Create your views here.

@login_required
def create_simulation(request):
    if request.method == 'POST':
        scenario = request.POST.get('scenario')
        
        # Créer une nouvelle simulation
        simulation = Simulation(
            user=request.user,
            scenario=scenario,
            status='created'
        )
        simulation.save()
        
        messages.success(request, 'Simulation créée avec succès!')
        return redirect('chatbot:chat', simulation_id=simulation.id)
    
    # Passer les choix de scénarios au template
    context = {
        'scenario_choices': Simulation.SCENARIO_CHOICES
    }
    return render(request, 'simulations/create_simulation.html', context)