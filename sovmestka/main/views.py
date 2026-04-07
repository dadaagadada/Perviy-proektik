from django.shortcuts import render, redirect
from .forms import PromptForm
from .models import *

def main(request):
    if request.method == 'POST':
        Prompt.objects.all().delete()
        return render(request, 'main/main.html')
    else:
        prompt = Prompt.objects.all()
        answer = Answer.objects.all()
        return render(request, 'main/main.html', {'prompts': prompt, 'answers': answer})

def create_prompt(request):
    if request.method == 'POST':
        form = PromptForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('main')
    else:
        form = PromptForm()
        return render(request, 'main/create_prompt.html', {'form': form})