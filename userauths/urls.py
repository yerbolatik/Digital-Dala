from django.urls import path
from django.contrib.auth import views as auth_views

from core.views import author, author_detail
from userauths import views


app_name = "userauths"

urlpatterns = [
    path('sign-up/', views.RegisterView, name='sign-up'),
    path('sign-in/', views.LoginView, name='sign-in'),
    path('logout/', views.LogoutView, name='logout'),

    path('author/', author, name='author'),
    path('author/<username>/', author_detail, name='author_detail'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile'),


    # path('profile/<username>', views.friend_profile, name='profile'),

    # path("profile-update/", views.profile_update, name="profile-update"),
    # path("delete-user/", views.delete_user, name="delete-user"),

    # # Tabs
    # path("friends-tab/", views.friends_tab, name="friends-tab"),

]
