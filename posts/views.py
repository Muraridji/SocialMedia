from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.urls import reverse
from .models import Post, Comment, Like
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.mixins import UserOwnerMixin
from posts.forms import PostForm, CommentForm
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from accounts.models import CustomUser

class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/post_list.html"


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)
        post = self.get_object()
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            if comment.content or comment.media:
                comment.save()
            return redirect('posts:post_detail', pk=post.pk)

        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "posts/post_form.html"
    form_class = PostForm
    success_url = reverse_lazy("posts:post_list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_update.html"
    success_url = reverse_lazy("posts:post_list")


class PostDeleteView(LoginRequiredMixin, UserOwnerMixin, DeleteView):
    model = Post
    template_name = "posts/post_delete_confirmation.html"
    success_url = reverse_lazy("posts:post_list")


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "posts/comment_delete_confirmation.html"

    def get_success_url(self):
        return reverse('posts:post_detail', kwargs={'pk': self.object.post.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return redirect('posts:post_detail', pk=obj.branch.pk)
        return super().dispatch(request, *args, **kwargs)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        media = request.FILES.get('media')
        parent_id = request.POST.get('parent_id')
        parent = Comment.objects.filter(id=parent_id).first() if parent_id else None

        if content or media:
            Comment.objects.create(
                post-post,
                author=request.user,
                content=content,
                media=media,
                parent=parent
            )

    return redirect('posts:post_detail', pk=pk)


@login_required
def toggle_post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('posts:post_detail', pk=pk)

@login_required
def toggle_comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, comment=comment)
    if not created:
        like.delete()
    return redirect('posts:post_detail', pk=comment.post.pk)


class UserPostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/user_posts.html"

    def get_queryset(self):
        return Post.objects.filter(creator__username=self.kwargs['username']).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewed_user'] = get_object_or_404(CustomUser, username=self.kwargs['username'])
        return context