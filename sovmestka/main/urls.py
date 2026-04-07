from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('create_prompt/', views.create_prompt, name='create_prompt'),
]