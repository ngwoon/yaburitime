from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('<str:whatboard>/', views.board, name='freeboard'),

    path('free/posting/', views.writingpost, name='writingfreepost'),
    path('secret/posting/', views.writingpost, name='writingsecretpost'),

    path('free/<int:pk>', views.postdetail, name='postdetail'),
    path('free/<int:pk>/recommend', views.recommend, name='recommend'),
    path('free/<int:pk>/unrecommend', views.unrecommend, name='unrecommend'),
]