from django.contrib import admin

from . models import *

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['number', 'time_stamp', 'miner', 'gase_used']
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['block', 'hash', 'from_address', 'to_address', 'value']
@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ['name', 'text']
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['prompt','text']