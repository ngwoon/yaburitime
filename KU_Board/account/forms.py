# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    name = forms.TextInput()
    nickname = forms.TextInput()

    REQUIRED_FIELD = [name, nickname]

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'name', 'nickname')

    def cleaned_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not password1 or not password2 or password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_password2())
        user.name = self.cleaned_data['name']
        user.nickname = self.cleaned_data['nickname']
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'name', 'nickname')
