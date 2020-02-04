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
        u = authenticate(username=request.POST['username'], password=request.POST['password'])
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
            return redirect('/board/free')
        else:
            print(form.error_messages)
            return HttpResponse('에러')


def signOut(request):
    logout(request)
    return redirect('board')
