from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Report


class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()

    class Meta:
        model=User
        fields=['username', 'email','password1', 'password2']

class UserUpdateForm(forms.ModelForm):

    email=forms.EmailField()

    class Meta:
        model=User
        fields=['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image', 'bio']

class ReportForm(forms.ModelForm):
    # reporter = forms.CharField(widget=forms.HiddenInput(), required=False, initial='reporter')
    # offender = forms.CharField(widget=forms.HiddenInput(), required=False, initial='offe')
    profanity = forms.BooleanField(required=False)
    discrimination = forms.BooleanField(required=False)
    inappropriate = forms.BooleanField(required=False)
    sexual = forms.BooleanField(required=False)
    bot = forms.BooleanField(required=False)
    message = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Bio here"}))
    class Meta:
        model = Report
        fields = ['profanity', 'discrimination', 'inappropriate', 'sexual', 'bot', 'message']
