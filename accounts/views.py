from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import CustomUser


def register(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, 'accounts/signup_page.html', {'form':form})

    elif request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    else:
        form = RegisterForm()
    return render(request, "accounts/signup_page.html", {"form":form})


from django.contrib import messages


def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'accounts/login_page.html', {'form': form})

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("accounts:home")
            else:
                messages.error(request, "Неправильное имя пользователя или пароль.")

        return render(request, "accounts/login_page.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("accounts:home")


@login_required
def user_profile_view(request, username):
    user_profile = get_object_or_404(CustomUser, username=username)
    return render(request, 'accounts/profile.html', {
        'user_profile': user_profile,
        'is_own_profile': user_profile == request.user,
    })


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:user-profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})



def home_view(request):
    return render(request, 'accounts/home.html')