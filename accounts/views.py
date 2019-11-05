from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password


def register(request):
    form = UserRegisterForm
    # Check if the form is a get method
    if request.method == "GET":
        context = {'form': form}
        return render(request, 'signup.html', context)
    # If this is a POST request then process the Form data
    elif request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = UserRegisterForm(request.POST)
        # Check if Form is valid
        if form.is_valid():
            getFormData = request.POST.copy()
            # Get the Users Username and Password and save it
            username = getFormData.get('username')
            newUser = form.save(commit=False)
            newUser.password = make_password(request.POST.get('password'))
            newRegisteredUser = form.save()
            # Register any new user as an Applicant
            my_group = Group.objects.get(name='Applicants')
            my_group.user_set.add(newRegisteredUser.id)
            user = User.objects.get(username=username)
            # Success message after submission
            messages.success(request, f'Account has been created for {user}! Log into your account and complete your profile')
            return redirect('login')
    else:
        # If this is a GET (or any other method) create the default form.
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})


# Handles the Profile view
@login_required(login_url=reverse_lazy('login'))
def profile(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        #  Gets the current logged in user's data
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        # Check if the forms are valid
        if u_form.is_valid and p_form.is_valid():
            # Save the forms
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        # If this is a GET (or any other method) create the default form.
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
            'u_form': u_form,
            'p_form': p_form
    }

    return render(request, 'profile.html', context)

