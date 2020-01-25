from django.shortcuts import render
from django.template import loader
# Create your views here.
from datetime import datetime
from .models import Post


def board(request):
    #template = loader.get_template('board/index.html')
    board_post = Post.objects.all()
    context = {
        'board_post':board_post
    }
    return render(request, 'board/board_index.html', context)
