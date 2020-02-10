from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from .models import CustomUser, Mail
from .forms import SignUpForm, CustomUserChangeForm
from django.contrib.auth import login, authenticate, logout


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

def signOut(request):
    logout(request)
    return redirect('home')

class MyPage(View):
    def get(self, request):
        if request.user.is_anonymous:
            return redirect('/')
        return render(request, 'account/mypage_index.html')

    def post(self, request):
        if request.user.is_anonymous:
            return redirect('/')
        return render(request, 'account/mypage_index.html')

class Msg(View):
    def get(self, request):
        if request.user.is_anonymous:
            return redirect('/')

        send_list = Mail.objects.filter(owner=request.user)
        receive_list = Mail.objects.filter(counter=request.user)

        counters=[]

        for msg in send_list:
            if msg.counter not in counters:
                counters.append(msg.counter)
        for msg in receive_list:
            if msg.owner not in counters:
                counters.append(msg.owner)

        return render(request, 'account/msg_index.html', {'msg_counters' : counters})

    def post(self, request):
        if request.user.is_anonymous:
            return redirect('/')

        counter = CustomUser.objects.get(nickname=request.POST.get('counter'))
        send_list = Mail.objects.filter(owner=request.user, counter=counter).order_by('datetime')
        receive_list = Mail.objects.filter(counter=request.user, owner=counter).order_by('datetime')
        messages = []

        slen = len(send_list)
        rlen = len(receive_list)
        sindex = 0
        rindex = 0
        while sindex != slen and rindex != rlen:
            if send_list[sindex].datetime < receive_list[rindex].datetime:
                messages.append({'content' : send_list[sindex].content, 'type' : 'send'})
                sindex += 1
            else:
                messages.append({'content' : receive_list[rindex].content, 'type' : 'receive'})
                rindex += 1

        if sindex == slen:
            while rindex != rlen:
                messages.append({'content' : receive_list[rindex].content, 'type' : 'receive'})
                rindex += 1
        else:
            while sindex != slen:
                messages.append({'content' : send_list[sindex].content, 'type' : 'send'})
                sindex += 1

        return render(request, 'account/msg_detail.html', {'msg_list' : messages, 'counter' : request.POST.get('counter')})


class SendMsg(View):
    def get(self, request):
        return render(request, 'account/msg_send.html')

    def post(self, request):
        pass


def update(request):
    if request.method == "POST":
        user = request.user
        user.name = request.POST["name"]
        user.nickname = request.POST["nickname"]
        user.save()
        return redirect('/')
    return render(request, 'account/mypage_update.html')


def delete(request):
    if request.method == "POST":
        request.user.delete()
        return redirect('/')
    return render(request, 'account/mypage_delete.html')
