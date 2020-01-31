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
from django.urls import reverse


def board(request,whatboard):


    if whatboard == 'free':
        board_post = Post.objects.filter(category=1).order_by('-boardNum')
        categorykr='자유게시판'
        categoryNum = 1

    elif whatboard == 'secret':
        board_post = Post.objects.filter(category=2).order_by('-boardNum')
        categorykr='비밀게시판'
        categoryNum = 2

    else:
        return redirect('/board/free/')

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
        'categorykr':categorykr,
        'categoryNum':categoryNum,
        'whatboard':whatboard
    }
    return render(request, 'board/board_index.html', context)


def writingpost(request,whatboard):

    if whatboard == 'free':
        category = 1
        changedwhatboard = '자유게시판'
    elif whatboard == 'secret':
        category = 2
        changedwhatboard = '비밀게시판'


    if request.method == "POST":
        form = Postform(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.nickname = '장유준'
            post.date = datetime.now()
            post.category = category

            post.save()
            pk = Post.objects.last().pk
            return redirect('/board/{}/{}'.format(whatboard,pk))
        else:
            messages.error(request, '제목 또는 내용이 입력되지 않았습니다.')
    else:
        form = Postform()

    context = {
        'form': form,
        'changedwhatboard': changedwhatboard,
        'whatboard':whatboard,
    }

    return render(request, 'board/board_post.html' ,context)


def postdetail(request,whatboard,pk):

    if whatboard == 'free':
        categorykr = '자유게시판'
    elif whatboard == 'secret':
        categorykr = '비밀게시판'

    board_post = Post.objects.get(pk=pk)
    context = {
        'board_post': board_post,
        'categorykr':categorykr,
        'whatboard':whatboard,
    }

    board_post.count_up()
    return render(request, 'board/board_detail.html', context)

def recommend(request,whatboard,pk):
   post = Post.objects.get(pk=pk)
   post.recommend += 1
   post.Field -= 1
   post.save()
   return postdetail(request,whatboard,pk)

def unrecommend(request,whatboard,pk):
   post = Post.objects.get(pk=pk)
   post.unrecommend += 1
   post.Field -= 1
   post.save()

   return postdetail(request,whatboard,pk)
