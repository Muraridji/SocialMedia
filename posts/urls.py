from django.urls import path
from posts import views

app_name = "posts"

urlpatterns = [
    path('post_list/', views.PostListView.as_view(), name="post_list"),
    path('post_create/', views.PostCreateView.as_view(), name="post_create"),
    path('<int:pk>/', views.PostDetailView.as_view(), name="post_detail"),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name="post_update"),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name="post_delete"),

    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment_delete'),

    path('<int:pk>/like/', views.toggle_post_like, name='post_like'),
    path('comment/<int:pk>/like/', views.toggle_comment_like, name='comment_like'),

    path('user/<str:username>/', views.UserPostListView.as_view(), name='user_posts'),
]
