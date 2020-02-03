from django.shortcuts import render
from django.shortcuts import redirect
from django.template import loader
# Create your views here.
from datetime import datetime
from .models import Post, Comment
from .forms import Postform, Commentform
from django.contrib import messages

from django.core.paginator import Paginator
from django.urls import reverse


def board(request, whatboard):
    if whatboard == 'free':
        board_post = Post.objects.filter(category=1).order_by('-boardNum')
        categorykr = '자유게시판'
        categoryNum = 1

    elif whatboard == 'secret':
        board_post = Post.objects.filter(category=2).order_by('-boardNum')
        categorykr = '비밀게시판'
        categoryNum = 2

    elif whatboard == 'hot':
        board_post = Post.objects.filter(recommendCount__gte=1).order_by('-boardNum')  # 추천수 n개 이상만 게시판에 표현
        categorykr = '인기게시판'
        categoryNum = 3

    else:
        return redirect('/board/free/')  # 없는 board로 접근시 자유게시판으로 자동 이동

    posts_of_page = 5  # 한 페이지당 나타낼 글의 개수
    paginator = Paginator(board_post, posts_of_page)
    page = request.GET.get('page')
    pageposts = paginator.get_page(page)
    prepage = paginator.get_page(page)
    nextpage = paginator.get_page(page)
    is_lastpage_hide = False

    if pageposts.number > 1:
        prepage = paginator.page(pageposts.number - 1)
    if pageposts.number < pageposts.paginator.num_pages:
        nextpage = paginator.page(pageposts.number + 1)

    if pageposts.number + 2 >= pageposts.paginator.num_pages:
        is_lastpage_hide = True

    request.session['page'] = pageposts.number  # 세션으로 페이지네이션 정보 넘김

    context = {
        'board_post': board_post,
        'pageposts': pageposts,
        'prepage': prepage,
        'nextpage': nextpage,
        'is_lastpage_hide': is_lastpage_hide,
        'categorykr': categorykr,
        'categoryNum': categoryNum,
        'whatboard': whatboard
    }
    return render(request, 'board/board_index.html', context)


def writingpost(request, whatboard):
    if whatboard == 'free':
        category = 1
        changedwhatboard = '자유게시판'
    elif whatboard == 'secret':
        category = 2
        changedwhatboard = '비밀게시판'
    elif whatboard == 'hot':
        category = 3
        changedwhatboard = '인기게시판'

    if request.method == "POST":

        form = Postform(request.POST)
        if form.is_valid():

            post = form.save(commit=False)
            post.user = request.user  # 현재 로그인 유저 획득
            post.date = datetime.now()
            post.category = category
            post.save()

            pk = Post.objects.last().pk
            return redirect('/board/{}/{}'.format(whatboard, pk))
        else:
            messages.error(request, '제목 또는 내용이 입력되지 않았습니다.')
    else:
        form = Postform()

    context = {
        'form': form,
        'changedwhatboard': changedwhatboard,
        'whatboard': whatboard,
    }

    return render(request, 'board/board_post.html', context)


def postdetail(request, whatboard, pk):
    if whatboard == 'free':
        categoryNum = 1
    elif whatboard == 'secret':
        categoryNum = 2
    elif whatboard == 'hot':
        categoryNum = 3

    if request.method == "POST":
        form = Commentform(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.date = datetime.now()
            comment.user = request.user
            comment.whatpost = Post.objects.get(pk=pk)
            comment.save()

            return redirect('/board/{}/{}'.format(whatboard, pk))
        else:
            messages.error(request, '내용을 입력해주세요')
    else:
        form = Commentform()

    board_post = Post.objects.get(pk=pk)
    comment = Comment.objects.filter(whatpost=board_post).order_by('date')

    if board_post.category == 1:
        categorykr = '자유게시판'
    elif board_post.category == 2:
        categorykr = '비밀게시판'
    elif board_post.category == 3:
        categorykr = '인기게시판'

    context = {
        'form': form,
        'board_post': board_post,
        'categorykr': categorykr,
        'whatboard': whatboard,
        'categoryNum': categoryNum,
        'comment': comment,
    }

    board_post.count_up()
    return render(request, 'board/board_detail.html', context)


def recommend(request, whatboard, pk):
    post = Post.objects.get(pk=pk)
    user = None
    for user in post.recommend.all():
        if user == request.user:
            post.recommend.remove(user)
            break;

    if user != request.user:
        post.recommend.add(request.user)  # recommend: many to many field 에 현재 추천한 user 정보 입력

    post.recommendCount = post.recommend.count()
    post.Field -= 1  # 조회수 감소
    post.save()
    return redirect('/board/{}/{}'.format(whatboard, pk))


def unrecommend(request, whatboard, pk):
    post = Post.objects.get(pk=pk)
    user = None

    for user in post.unrecommend.all():
        if user == request.user:
            post.unrecommend.remove(user)
            break

    if user != request.user:
        post.unrecommend.add(request.user)  # unrecommend: many to many field 에 현재 추천한 user 정보 입력
    post.Field -= 1
    post.unrecommendCount = post.unrecommend.count()
    post.save()

    return redirect('/board/{}/{}'.format(whatboard, pk))


def deletepost(request, whatboard, pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.user:
        post.delete()

    return redirect('/board/{}'.format(whatboard))


def deletecomment(request, whatboard, pk, commentnumber):
    comment = Comment.objects.get(pk=commentnumber)
    if request.user == comment.user:
        comment.delete()

    return redirect('/board/{}/{}'.format(whatboard, pk))


def edit(request, whatboard, pk):
    if whatboard == 'free':
        changedwhatboard = '자유게시판'
    elif whatboard == 'secret':
        changedwhatboard = '비밀게시판'
    elif whatboard == 'hot':
        changedwhatboard = '인기게시판'

    if request.method == "POST":

        form = Postform(request.POST)
        if form.is_valid():

            thispost = Post.objects.get(pk=pk)
            post = form.save(commit=False)
            thispost.title = post.title
            thispost.content = post.content
            thispost.save()

            return redirect('/board/{}/{}'.format(whatboard, pk))
        else:
            messages.error(request, '제목 또는 내용이 입력되지 않았습니다.')
    else:
        form = Postform()

    context = {
        'thispost': Post.objects.get(pk=pk),
        'form': form,
        'changedwhatboard': changedwhatboard,
        'whatboard': whatboard,
    }

    return render(request, 'board/board_edit.html', context)