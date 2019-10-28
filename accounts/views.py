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
    elif request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            getFormData = request.POST.copy()
            username = getFormData.get('username')
            newUser = form.save(commit=False)
            newUser.password = make_password(request.POST.get('password'))
            newRegisteredUser = form.save()
            # Register any new user as an Applicant
            my_group = Group.objects.get(name='Applicants')
            my_group.user_set.add(newRegisteredUser.id)
            user = User.objects.get(username=username)

            messages.success(request, f'Account has been created for {user}! Log into your account and complete your profile')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url=reverse_lazy('login'))
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
            'u_form': u_form,
            'p_form': p_form
    }

    return render(request, 'profile.html', context)

