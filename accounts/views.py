from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .models import CustomUser, FriendshipRequest, Friendship


def home_view(request):
    return render(request, 'accounts/home.html')


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
    requests = user_profile.received_requests.all()
    return render(request, 'accounts/profile.html', {
        'user_profile': user_profile,
        'is_own_profile': user_profile == request.user,
        'received_requests': requests,
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


#Views for friends interaction

class SendFriendRequestView(LoginRequiredMixin, View):
    def get(self, request, username):
        receiver = get_object_or_404(CustomUser, username=username)
        if receiver == request.user:
            messages.error(request, "Не можна надіслати запит самому собі.")
        elif Friendship.are_friends(request.user, receiver):
            messages.info(request, "Ви вже є друзями.")
        elif FriendshipRequest.objects.filter(sender=request.user, receiver=receiver).exists():
            messages.info(request, "Запит уже надіслано.")
        else:
            FriendshipRequest.objects.create(sender=request.user, receiver=receiver)
            messages.success(request, f"Запит дружби надіслано {receiver.username}.")
        return redirect('accounts:user_list')


class AcceptFriendRequestView(LoginRequiredMixin, View):
    def get(self, request, request_id):
        friend_request = get_object_or_404(FriendshipRequest, id=request_id, receiver=request.user)
        Friendship.objects.create(user1=request.user, user2=friend_request.sender)
        friend_request.delete()
        messages.success(request, f"Ви тепер друзі з {friend_request.sender.username}.")
        return redirect('accounts:friend_request')


class DeclineFriendRequestView(LoginRequiredMixin, View):
    def get(self, request, request_id):
        friend_request = get_object_or_404(FriendshipRequest, id=request_id, receiver=request.user)
        friend_request.delete()
        messages.info(request, "Запит дружби відхилено.")
        return redirect('accounts:friend_request')


class RemoveFriendView(LoginRequiredMixin, View):
    def get(self, request, username):
        friend = get_object_or_404(CustomUser, username=username)
        Friendship.objects.filter(user1=request.user, user2=friend).delete()
        Friendship.objects.filter(user1=friend, user2=request.user).delete()
        messages.success(request, f"{friend.username} видалено з друзів.")
        return redirect('accounts:user_profile', username=username)


class FriendRequestsView(LoginRequiredMixin, ListView):
    model = FriendshipRequest
    context_object_name = 'incoming_requests'
    template_name = 'accounts/friend_request.html'

    def get_queryset(self):
        return self.request.user.received_requests.all()


class FriendsListView(LoginRequiredMixin, View):
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        friends1 = Friendship.objects.filter(user1=user).values_list('user2', flat=True)
        friends2 = Friendship.objects.filter(user2=user).values_list('user1', flat=True)
        friends_ids = list(friends1) + list(friends2)
        friends = CustomUser.objects.filter(id__in=friends_ids)
        return render(request, 'accounts/friends_list.html', {
            'friends': friends,
            'profile_user': user
        })


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return CustomUser.objects.exclude(id=self.request.user.id)