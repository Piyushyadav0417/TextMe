from django.urls import path
from .views import *
urlpatterns = [
    path('', HomeView, name='home_page'),
    path('register/', RegisterView, name='register_page'),
    path('login/', LoginView, name='login_page'),
    path('logout/', LogoutView, name='logout_page'),
    path("search/", SearchUserView, name="search_page"),
    # path("chat/<str:username>/", StartChatView, name="start_chat"),
    path("myprofile/", MyProfileView, name="myprofile_page"),
    path("userprofile/<str:username>/", UserProfile, name='userprofile_page'),
    # path("chat/<str:username>/", chat_view, name="chat_view"),
    path("chat/<str:username>/", chat_room, name="chat_room"),
]
