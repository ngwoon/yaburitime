from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from .models import CustomUser
from .forms import SignUpForm
from django.contrib.auth import login, authenticate, logout
# Create your views here.


class SignIn(View):

    def get(self, request):
        return render(request, 'account/signin.html')

    def post(self, request):
        u = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if u:
            login(request, user=u)
            return redirect('/board/free/')

        return render(request, 'account/signin.html')


class SignUp(View):
    def get(self, request):
        form = SignUpForm(request.POST)
        return render(request, 'account/signup.html', {'form' : form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            id_dup = CustomUser.objects.filter(username=form.cleaned_data['username'])
            nickname_dup = CustomUser.objects.filter(nickname=form.cleaned_data['nickname'])
            
            if id_dup == None:
                return HttpResponse('아이디 중복입니다.')
            if nickname_dup == None:
                return HttpResponse('닉네임 중복입니다.')

            form.save()

            u = authenticate(username=request.POST.get('username'), password=request.POST.get('password1'))
            if u:
                login(request, user=u)
                return redirect('/board/free/')
            return redirect('home')
        else:
            return HttpResponse('입력 형식이 잘못되었습니다. 글자 제한을 잘 지켜주세요')


class MyPage(View):
    def get(self, request):
        return render(request, 'account/mypage_index.html')

    def post(self, request):
        return render(request, 'account/mypage_index.html')


def signOut(request):
    logout(request)
    return redirect('home')
