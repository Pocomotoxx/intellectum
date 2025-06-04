from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Profile is created automatically by signals, now update it if needed
            # For now, we'll let them fill the profile details in the edit profile section
            login(request, new_user)
            return redirect('profile_edit') # Redirect to profile edit page after registration
        else:
            # Add print for debugging in subtask if form is not valid
            print(f"User form errors: {user_form.errors.as_json()}")
    else:
        user_form = UserRegistrationForm()
    return render(request, 'profiles/signup.html', {'user_form': user_form})

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profiles/profile_detail.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile_view')
        else:
            # Add print for debugging in subtask if form is not valid
            print(f"Profile form errors: {profile_form.errors.as_json()}")
    else:
        profile_form = ProfileForm(instance=profile)
    return render(request, 'profiles/profile_edit.html', {'profile_form': profile_form})
