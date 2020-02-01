# users/admin.py
from django.contrib import admin
<<<<<<< HEAD:KU_Board/account/admin.py
from .models import User

# from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(User)
=======
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['name', 'nickname',]

admin.site.register(CustomUser, CustomUserAdmin)
>>>>>>> dev-join:KU_Board/join/admin.py
