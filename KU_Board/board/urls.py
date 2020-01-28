from django.urls import path
from . import views

urlpatterns = [
    path('', views.board, name='board'),
    path('posting/', views.writingpost, name='writingpost'),
    path('<int:pk>', views.postdetail, name='postdetail'),
    path('<int:pk>/recommend', views.recommend, name='recommend'),
    path('<int:pk>/unrecommend', views.unrecommend, name='unrecommend'),
]