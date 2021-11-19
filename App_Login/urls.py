from django.urls import path

from .views import sign_Up, login_Page, edit_Profile, logout_User, profile, user, follow, unfollow

app_name = "App_Login"

urlpatterns = [
    path('signup/', sign_Up, name='sign_up'),
    path('login/', login_Page, name='login'),
    path('edit/', edit_Profile, name='edit'),
    path('logout/', logout_User, name='logout'),
    path('profile/', profile, name='profile'),
    path('user/<username>/', user, name='user'),
    path('follow/<username>/', follow, name='follow'),
    path('unfollow/<username>/', unfollow, name='unfollow'),


]





