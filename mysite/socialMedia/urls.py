from django.urls import path
from .views import *
from django.contrib.auth import views as auth_view

app_name = 'socialMedia'

urlpatterns =  [
    path('',index),
    path('register/',register,name='register'),
    # path('login/',user_login,name='user_login'),
    path('login/',auth_view.LoginView.as_view(),name='user_login'),
    path('password/change/',passwordChangeView.as_view(),name='password_change'),
    path('password/change/done',auth_view.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('homepage/',homepage,name='homepage'),
    # path('logout/',user_logout,name='user_logout'),
    path('logout/',auth_view.LogoutView.as_view(),name='user_logout'),
    path('addPost/',add_post,name='add_post'),
    path('drafts/',retrieve_drafts,name='drafts'),
    path('publish/<int:id>/',publish,name='publish'),
    path('draft/<int:id>',change_to_draft,name='change_to_draft'),
    path('published/',retrieve_published,name='published'),
    path('update/<int:id>/',update,name='update'),
    path('delete/<int:id>/',delete,name='delete'),
    path('profile_data/',profile_data,name='profile_data'),
    path('post/<int:id>/',see_complete_post,name='complete_post'),
    path('post/like/<int:id>/',like,name='like'),
    path('post/dislike/<int:id>/',dislike,name='dislike'),
    path('post/search/<str:username>/',search,name='search'),
    path('get/user/<int:id>/',get_user,name='getUser'),
    path('see/published/post/<int:id>',see_published_post,name='seePubPost'),
    path('follow/<int:id>/',follower,name='follow'),
    path('friend/request',friend_request,name='friend_request'),
    path('accept/<int:id>',accept,name='accept'),
    path('reject/<int:id>',reject,name='reject'),
    path('list/follower/',list_of_follower,name='list_of_follower'),
    path('list/following/',following,name='list_of_following'),
    path('news_feed/',news_feed,name='news_feed'),
]