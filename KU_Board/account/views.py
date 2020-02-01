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

        u = authenticate(username=request.POST['id'], password=request.POST['pw'])

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
            form.save()
            return redirect('board')
        else:
            return HttpResponse('사용자명이 이미 존재합니다.')


def signOut(request):
    logout(request)
    return redirect('board')