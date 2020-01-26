from django.urls import path
from . import views

urlpatterns = [
    path('', views.board, name='board'),
    path('posting/', views.writingpost, name='writingpost'),

]