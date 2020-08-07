from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView, RedirectView
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, AccountAuthenticationForm, UserUpdateForm, ProfileUpdateForm
from accounts.models import User
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate
import urllib.parse
import sweetify


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            sweetify.success(request, title='Account Created', text='Your account has been created, log in and complete your profile', icon='success', button='Ok', timer=3000)
            return redirect('login')
        else:
            return render(request, 'signup.html', {'form': form})


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)


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
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if request.user.profile.birth_date is None or request.user.profile.phone_number is None or request.user.profile.sex is None:
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
