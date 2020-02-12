# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import SignUpForm, CustomUserChangeForm
from .models import CustomUser, Mail

class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'password', 'name', 'nickname',]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Mail)
