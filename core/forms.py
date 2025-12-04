from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserCreationForm 
from .models import User

# 1. Sign-Up Form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'})
    )
    location = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Your City or ZIP Code'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "location")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['username'].widget.attrs.update({'placeholder': 'Choose a username'})

# 2. Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Your Username', 'class': 'form-control'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Your Password', 'class': 'form-control'}
        )
    )