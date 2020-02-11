from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from .models import CustomUser, Mail
from .forms import SignUpForm, SendForm
from django.contrib.auth import login, authenticate, logout

from django.core.exceptions import ObjectDoesNotExist

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
        form = SendForm()
        return render(request, 'account/msg_send.html', {'form' : form})

    def post(self, request):
        if request.POST.get('counter') == request.user.nickname:
            return HttpResponse('자기 자신에게는 쪽지를 보낼 수 없습니다.')

        post_mutable = request.POST._mutable
        request.POST._mutable = True

        try:
            counter = CustomUser.objects.get(nickname=request.POST.get('counter'))
            request.POST['counter'] = counter
            request.POST._mutable = post_mutable

        except ObjectDoesNotExist:
            return HttpResponse('해당 닉네임을 가진 사용자는 존재하지 않습니다.')

        form = SendForm(request.POST)
        if form.is_valid():
            send = form.save(commit=False)
            send.owner = request.user
            send.save()
            return redirect('home')
        else:
            return HttpResponse('상대 닉네임과 내용은 필수 항목입니다. 상대 닉네임과 내용을 채웠음에도 오류가 발생한다면 관리자에게 문의 바랍니다.')

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
