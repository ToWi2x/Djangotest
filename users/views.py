from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm,ProfileUpdateForm


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from itreporting.models import Issues  # Correct import (make sure it's 'Issues', not 'Issue')
from .models import Profile




def register(request):
 if request.method == 'POST':
  form = UserCreationForm(request.POST)
  if form.is_valid():
     form.save()
     username = form.cleaned_data.get('username')
     messages.success(request, f'Account created for {username}!')
     return redirect('itreporting:home')
  else:
   messages.warning(request, 'Unable to create account.')
 else:
    form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Student Registration'})

    messages.success(request, f'Your account has been created! Now you can login!') 
    return redirect('login') 
 
 
@login_required
def profile(request):
    # Retrieve or create the profile associated with the user
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()  # Save updated user info
            p_form.save()  # Save updated profile info
            messages.success(request, 'Your account has been successfully updated!')
            return redirect('profile')  # Redirect to the profile page after update
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {'u_form': u_form, 'p_form': p_form, 'title': 'Student Profile'}
    return render(request, 'users/profile.html', context)



@login_required
def report(request):
    # Logic for handling the report page
    return render(request, 'users/report.html', {'title': 'Report'})


