from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'Choose_banner', 'About_you', 'Write_your_bio', 'Add_current_title', 'Add_current_employer', 'Add_an_education_credential', 'Choose_gender', 'Home_details', 'Current_city', 'Current_address', 'Add_hometown', 'External_links', 'Add_Facebook', 'Add_Twitter', 'Add_YouTube', 'Add_Instagram', 'Add_your_personal_website']


class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []
    # forms w/ empty field