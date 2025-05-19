from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("signup_page/", views.register, name="signup"),
    path("login_page/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('profile/edit-profile/', views.edit_profile_view, name='edit-profile'),
    path('profile/<str:username>/', views.user_profile_view, name='user-profile'),
    path('', views.home_view, name='home'),
]