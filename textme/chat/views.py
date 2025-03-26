from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import *
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
@login_required(login_url='login_page')
def HomeView(request):
    return render(request, 'chat/home.html')  # Send pizzas to template


def RegisterView(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'User already exist with thhis username')
            return redirect('register_page')
        
        user = User.objects.create_user(
            first_name=first_name,
            username=username,
            password=password
        )
        user.save()
        return redirect("login_page")

    return render(request, "authentication/register.html")


def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home_page")  # Redirect to home page (Change if needed)
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "authentication/login.html")

@login_required(login_url='login_page')
def LogoutView(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect("login_page")

@login_required(login_url='login_page')
def SearchUserView(request):
    query = request.GET.get('q', '')

    users = User.objects.filter(username__icontains=query) if query else []

    return render(request, "chat/search.html", {"users": users, "query": query})

@login_required(login_url='login_page')
def UserProfile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "chat/userprofile.html", {"user": user})

@login_required(login_url='login_page')
def MyProfileView(request):
    return render(request, "chat/myprofile.html", {"user": request.user})


def chat_room(request, username):
    other_user = get_object_or_404(User, username=username)  # Ensure user exists
    room_name = get_room_name(request.user, other_user)  # Unique room name

    # Fetch chat history (messages where sender=logged-in user and receiver=other user OR vice versa)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user], 
        receiver__in=[request.user, other_user]
    ).order_by("timestamp")  # Oldest messages first

    return render(request, "chat/chat_room.html", {
        "room_name": room_name,
        "other_user": other_user,
        "messages": messages  # Send messages to template
    })
# def chat_room(request, username):
#     other_user = get_object_or_404(User, username=username)  # ✅ Ensure user exists
#     room_name = get_room_name(request.user, other_user)  # ✅ No `.user` needed

#     return render(request, "chat/chat_room.html", {"room_name": room_name, "other_user": other_user})


def get_room_name(user1, user2):
    """Generate a unique chat room name for two users"""
    usernames = sorted([user1.username, user2.username])  # Sort to ensure same order
    return f"chat_{usernames[0]}_{usernames[1]}"
