from django.shortcuts import render
from django.shortcuts import redirect
from django.template import loader
# Create your views here.
from datetime import datetime
from .models import Post
from .forms import Postform
from django.utils import timezone
from django.contrib import messages



def board(request):
    #template = loader.get_template('board/index.html')
    board_post = Post.objects.all()
    context = {
        'board_post':board_post,
    }
    return render(request, 'board/board_index.html', context)


def writingpost(request):
    if request.method == "POST":
        form = Postform(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.nickname = '장유준'
            post.date = datetime.now()
            post.save()
            return redirect('/board/', pk=post.pk)
        else:
            messages.info(request, '제목 또는 내용이 입력되지 않았습니다.')
    else:
        form = Postform()
    return render(request, 'board/posting.html', {'form': form})

    # post = Post()
    # post.title = form.cleaned_data['title']
    # post.content = form.cleaned_data['content']
    # post.save()
