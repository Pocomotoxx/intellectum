from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password_confirm(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_confirm']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password_confirm']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'short_bio', 'favorite_books', 'favorite_movies', 'favorite_music_genres', 'profile_picture_url']
