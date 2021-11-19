from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import CreateNewUser, EditProfile
from .models import UserProfile, Follow
from App_Posts.forms import PostForm 
import App_Posts



def sign_Up(request):
    if request.user.is_authenticated and request.user.is_active:
        return HttpResponseRedirect(reverse('App_Posts:home'))
        
    form = CreateNewUser()
    registered = False
    if request.method == 'POST':
        form = CreateNewUser(data=request.POST)
        if form.is_valid():
            user = form.save()
            registered = True
            user_profile = UserProfile(user=user)
            user_profile.save()
            return HttpResponseRedirect(reverse('App_Login:login'))

    context = {
        'title': 'Signup Form Here',
        'form': form,
    }

    return render(request, 'App_Login/signup.html', context)




def login_Page(request):
    if request.user.is_authenticated and request.user.is_active:
        return HttpResponseRedirect(reverse('App_Posts:home'))

    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_Posts:home'))


    context = {
        'title': 'Login Page',
        'form': form,
        
    }

    return render(request, 'App_Login/login.html', context)




@login_required
def edit_Profile(request):

    current_user = UserProfile.objects.get(user=request.user)

    form = EditProfile(instance=current_user)

    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=current_user)

        if form.is_valid():
            form.save(commit=True)

            form = EditProfile(instance=current_user)
            return HttpResponseRedirect(reverse('App_Login:profile'))


    context = {
        'title': 'Edit Profile Page',
        'form': form,
    }

    return render(request, 'App_Login/profile.html',context)




@login_required
def logout_User(request):

    logout(request)

    return HttpResponseRedirect(reverse('App_Login:login'))




@login_required
def profile(request):

    form = PostForm()
    if request.method == 'POST':

        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return HttpResponseRedirect(reverse('home'))


    context = {
        'title':'User Profile',
        'form': form,
    }

    return render(request, 'App_Login/user.html', context)




@login_required
def user(request, username):

    user_other = User.objects.get(username=username)

    already_followed = Follow.objects.filter(follower=request.user, following=user_other)
    if user == request.user:
        return HttpResponseRedirect(reverse('App_Login:profile'))

    context = {
        'title': 'User Profile Page',
        'user_other': user_other,
        'already_followed': already_followed,
    }

    return render(request, 'App_Login/user_other.html', context)




@login_required
def follow(request, username):

    following_user = User.objects.get(username=username)
    follower_user = request.user

    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    
    if not already_followed:
        followed_user = Follow(follower=follower_user, following=following_user)
        followed_user.save()

    return HttpResponseRedirect(reverse('App_Login:user', kwargs={'username':username}))




@login_required
def unfollow(request, username):

    following_user = User.objects.get(username=username)
    follower_user = request.user

    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    already_followed.delete()

    return HttpResponseRedirect(reverse('App_Login:user', kwargs={'username': username}))











