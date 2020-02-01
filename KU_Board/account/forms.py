from .models import User

from django import forms


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'pw', 'username', 'nickname']
