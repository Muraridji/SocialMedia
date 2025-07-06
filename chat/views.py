from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from .models import Chat, Message
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ChatForm, MessageForm, GroupChatForm
from django.db.models import Count

from django.views import View
from django.contrib import messages

from accounts.models import CustomUser


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    context_object_name = "chats"
    template_name = "chat/chat_list.html"

    def get_queryset(self):
        queryset = super().get_queryset().exclude(username=self.request.user.username)
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(username__icontains=search_query)
        return queryset


class UserListView(ListView):
    model = CustomUser
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_count'] = self.get_queryset().count()
        return context

    def get_queryset(self):
        queryset = super().get_queryset().exclude(id=self.request.user.id)
        search_query = self.request.GET.get('search', '').strip()
        print(f"Search query: '{search_query}'")
        if search_query:
            filtered_qs = queryset.filter(username__icontains=search_query)
            print(f"Filtered count: {filtered_qs.count()}")
            return filtered_qs
        print(f"Total count: {queryset.count()}")
        return queryset


class ChatDetailView(DetailView):
    model = Chat
    context_object_name = "chats"
    template_name = "chat/chat_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message_form'] = MessageForm()
        context['messages'] = self.object.messages.order_by('created_at')
        return context

    def post(self, request, *args, **kwargs):
        message_form = MessageForm(request.POST, request.FILES)
        chat = self.get_object()
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.author = request.user
            message.chat = chat
            if message.content or message.media:
                message.save()
            return redirect('chat:chat_detail', pk=chat.id)

        context = self.get_context_data()
        context['comment_form'] = message_form
        return self.render_to_response(context)


class PrivateChatCreateView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        second_user = get_object_or_404(CustomUser, id=user_id)

        #seek for existed chat between users
        chats = Chat.objects.filter(
            group_chat=False,
            participants=request.user
        ).filter(
            participants=second_user
        )

        if chats.exists():
            return redirect('chat:chat_detail', pk=chats.first().pk)

        # if no - create new chat
        chat = Chat.objects.create(group_chat=False)
        chat.participants.set([request.user, second_user])

        return redirect('chat:chat_detail', pk=chat.pk)




class GroupChatCreateView(LoginRequiredMixin, CreateView):
    model = Chat
    form_class = GroupChatForm
    template_name = "chat/group_chat_create.html"

    def form_valid(self, form):
        form.instance.group_chat = True
        response = super().form_valid(form)

        self.object.participants.add(self.request.user)
        self.object.admins.add(self.request.user)
        return response

    def get_success_url(self):
        return reverse_lazy('chat:chat_detail', kwargs={'pk': self.object.pk})


class JoinGroupChatView(LoginRequiredMixin, View):
    def post(self, request, pk):
        chat = get_object_or_404(Chat, pk=pk, group_chat=True)
        if request.user not in chat.participants.all():
            chat.participants.add(request.user)
            messages.success(request, "Ви приєдналися до групи.")
        else:
            messages.info(request, "Ви вже учасник цієї групи.")
        return redirect('chat:chat_detail', pk=pk)


class LeaveGroupChatView(LoginRequiredMixin, View):
    def post(self, request, pk):
        chat = get_object_or_404(Chat, pk=pk, group_chat=True)
        if request.user in chat.participants.all():
            chat.participants.remove(request.user)
            messages.success(request, "Ви покинули групу.")
        else:
            messages.info(request, "Ви не учасник цієї групи.")
        return redirect('chat:chat_list')