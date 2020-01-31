from django import forms
from .models import Post,Comment


class Postform(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content',)
        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력하세요.'}),
        #     'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '내용을 입력하세요.'}),
        # }
        # }


class Commentform(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)