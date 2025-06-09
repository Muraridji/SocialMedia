from django.urls import path
from chat import views

app_name = "chat"

urlpatterns = [
    path('chat_list', views.ChatListView.as_view(), name='chat_list'),
    path('<int:pk>/', views.ChatDetailView.as_view(), name='chat_detail'),
    path('start/<int:user_id>/', views.PrivateChatCreateView.as_view(), name='create_private_chat'),
    path('group/create/', views.GroupChatCreateView.as_view(), name='group_chat_create'),
    path('group/<int:pk>/join/', views.JoinGroupChatView.as_view(), name='join_group_chat'),
    path('group/<int:pk>/leave/', views.LeaveGroupChatView.as_view(), name='leave_group_chat'),
]