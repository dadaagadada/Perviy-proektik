from django.forms import ModelForm
from .models import *


class PromptForm(ModelForm):
    class Meta:
        model = Prompt
        fields = ['name', 'text']