from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import User, Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Tên đăng nhập")
    password = forms.CharField(widget=forms.PasswordInput)


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
        