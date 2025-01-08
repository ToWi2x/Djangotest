from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from itreporting.models import Issues  # Importing Issues from the correct app

# User Registration Form (to create a new user)
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email address', help_text='Your SHU email address.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


# User Update Form (to update user details)
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Email address', help_text='Your SHU email address.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        # Removed password1 and password2 because you don't want to update password here.


# Profile Update Form (to update profile info, such as the image)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'address', 'city', 'country', 'image']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter address'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter city/town'}),
            'country': forms.TextInput(attrs={'placeholder': 'Enter country'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Full Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=200, label="Subject", widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), label="Your Message")

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issues  # Reference the correct model (Issues)
        fields = ['issue_type', 'description', 'assigned_to', 'priority', 'status', 'reported_by', 'room', 'urgent']  # Include fields that exist in the Issues model
