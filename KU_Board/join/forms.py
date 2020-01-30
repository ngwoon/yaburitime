from .models import User

from django import forms

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'pw', 'username', 'nickname']
        widgets = {
            'id': forms.TextInput(attrs={'placeholder': '아이디는 5자 이상 입력해야 합니다.'}),
            'pw': forms.TextInput(attrs={'placeholder': '비밀번호는 8자 이상이어야 합니다.'}),
            'username': forms.TextInput(),
            'nickname': forms.TextInput(attrs={'placeholder': '닉네임은 2자 이상이어야 합니다.'}),
        }