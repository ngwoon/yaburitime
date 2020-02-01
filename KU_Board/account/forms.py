# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('name', 'nickname')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('name', 'nickname')


class SignUpForm(forms.ModelForm):
    class Meta:
<<<<<<< HEAD:KU_Board/account/forms.py
        model = User
        fields = ['id', 'pw', 'username', 'nickname']
=======
        model = CustomUser
        fields = ('name', 'nickname')
>>>>>>> dev-join:KU_Board/join/forms.py
