from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with the URL name of your home page
        else:
            # Invalid credentials, display an error message
            error_message = 'Invalid username or password. Please try again.'
            return render(request, 'authenticate/login.html', {'error_message': error_message})

    return render(request, 'authenticate/login.html')


def logout_view(request):
    logout(request)
    message = "You have been logged out successfully."
    return redirect('home')  # Replace 'home' with the desired URL to redirect after logout


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful. You have been logged in.')
            return redirect('home')
    else:
        form = RegisterUserForm()

    context = {
        'form': form
    }
    return render(request, 'authenticate/register_user.html', context)
