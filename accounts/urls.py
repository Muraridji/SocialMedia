from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    #Users
    path("signup_page/", views.register, name="signup"),
    path("login_page/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('profile/edit-profile/', views.edit_profile_view, name='edit-profile'),
    path('profile/<str:username>/', views.user_profile_view, name='user-profile'),

    #Friends
    path('send-request/<str:username>/', views.SendFriendRequestView.as_view(), name='send_request'),
    path('accept-request/<int:request_id>/', views.AcceptFriendRequestView.as_view(), name='accept_request'),
    path('decline-request/<int:request_id>/', views.DeclineFriendRequestView.as_view(), name='decline_request'),
    path('remove-friend/<str:username>/', views.RemoveFriendView.as_view(), name='remove_friend'),
    path('requests/', views.FriendRequestsView.as_view(), name='friend_request'),
    path('friends/<str:username>/', views.FriendsListView.as_view(), name='friends_list'),
    path('users/', views.UserListView.as_view(), name='user_list'),
]