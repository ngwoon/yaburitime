from django.shortcuts import render
from django.shortcuts import redirect
from .forms import Lessonform


def calculator(request):

    if request.method == "POST":

        form = Lessonform(request.POST)
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

