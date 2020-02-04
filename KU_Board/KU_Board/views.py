from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View

# 로그인 세션에 따라 template_name이 index.html 혹은 board_index.html로 이동
class HomeView(View):
    def get(self, request):
        if request.user.is_anonymous:
            return render(request, 'index.html')
        else:
            return redirect('board/free/')


    def post(self, request):
        if request.user.is_anonymous:
            return render(request, 'index.html')
        else:
            return redirect('board/free/')
