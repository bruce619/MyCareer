from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, AccountAuthenticationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
import urllib.parse
import sweetify


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
            sweetify.success(request, title='Account Created', text='Your account has been created, log in and complete your profile', icon='success', button='Ok', timer=3000)
            return redirect('login')
    else:
        # If this is a GET (or any other method) create the default form.
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    redirect_to = urllib.parse.unquote(request.GET.get('next', 'home'))
    form = AccountAuthenticationForm
    # Check if the form is a get method
    if request.method == "GET":
        context = {'form': form}
        return render(request, 'registration/login.html', context)
    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                if request.user.profile.date_of_birth is None or request.user.profile.phone_number is None or request.user.profile.sex is None:
                    sweetify.info(request, title='Update Profile', text='Kindly complete your profile', icon='info', button='Ok', timer=5000)
                    return redirect("profile")
                else:
                    return redirect(redirect_to)

    else:
        form = AccountAuthenticationForm()

    return render(request, "registration/login.html", {'form': form})


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
            sweetify.success(request, title='Account Updated', text='Your account has been updated!', icon='success', button='Ok', timer=3000)
            return redirect('home')
    else:
        # If this is a GET (or any other method) create the default form.
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
            'u_form': u_form,
            'p_form': p_form
    }

    return render(request, 'profile.html', context)
