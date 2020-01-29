from django.shortcuts import render
from django.shortcuts import redirect
from django.template import loader
# Create your views here.
from datetime import datetime
from .models import Post
from .forms import Postform
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator



def board(request):
    board_post = Post.objects.all().order_by('-boardNum')

    posts_of_page = 5 # 한 페이지당 나타낼 글의 개수
    paginator = Paginator(board_post, posts_of_page)
    page = request.GET.get('page')
    pageposts = paginator.get_page(page)
    prepage = paginator.get_page(page)
    nextpage = paginator.get_page(page)
    is_lastpage_hide = False

    if pageposts.number > 1:
        prepage = paginator.page(pageposts.number-1)
    if pageposts.number < pageposts.paginator.num_pages:
        nextpage =paginator.page(pageposts.number+1)

    if pageposts.number+2 >= pageposts.paginator.num_pages:
            is_lastpage_hide = True

    context = {
        'board_post':board_post,
        'pageposts':pageposts,
        'prepage':prepage,
        'nextpage':nextpage,
        'is_lastpage_hide':is_lastpage_hide,
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
            messages.error(request, '제목 또는 내용이 입력되지 않았습니다.')
    else:
        form = Postform()
    return render(request, 'board/posting.html', {'form': form})


def postdetail(request,pk):
    board_post = Post.objects.get(pk=pk)
    context = {
        'board_post': board_post,
    }
    board_post.count_up()
    return render(request, 'board/post_detail.html', context)

def recommend(request,pk):
   post = Post.objects.get(pk=pk)
   post.recommend += 1
   post.Field -= 1
   post.save()
   return postdetail(request,pk)

def unrecommend(request,pk):
   post = Post.objects.get(pk=pk)
   post.unrecommend += 1
   post.Field -= 1
   post.save()

   return postdetail(request,pk)
