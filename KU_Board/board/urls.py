from django.urls import path
from . import views

urlpatterns = [
    path('', views.board, name='board'),
    path('elements/', views.elements, name='elements'),
    path('generic/', views.generic, name='generic'),

]