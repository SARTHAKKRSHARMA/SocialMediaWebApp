import os
from os import environ
from .decorators import isProfileCreated
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.shortcuts import render
from django.contrib.auth.admin import User
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth.views import PasswordChangeView
# Create your views here.


def index(request):
    return HttpResponseRedirect(reverse('socialMedia:user_login'))

def register(request):
    if(request.method=='GET'):
        form = UserForm()
        return render(request,'register.html',{'form':form})
    
    if(request.method=='POST'):
        form = UserForm(request.POST)
        if(form.is_valid()):
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User(username=username,password=password)
            user.set_password(user.password)
            user.save()
            profile = Profile(user=user)
            profile.save()
            return render(request,'success.html',{'user':user})
        else:
            return HttpResponseRedirect(reverse('socialMedia:register'))


def user_login(request):
    if(request.method =='GET'):
        form = UserForm()
        return render(request,'login.html',{'form':form})

    if(request.method =='POST'):
        form = UserForm(request.POST)
        if(form.is_valid):
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username,password=password)
            if(user):
                logged = login(request,user)
                return HttpResponseRedirect(reverse('socialMedia:homepage'))
            return HttpResponse("Incorrect Credentials")
        return HttpResponseRedirect(reverse('user_login'))

@login_required
@isProfileCreated
def homepage(request):
    posts = Post.objects.filter(status='published').order_by('-number_of_likes','-publish')[:5]
    newest_posts = Post.objects.filter(status='published').order_by('-publish')[:5]
    most_commented_posts = Post.objects.filter(status='published').order_by('-number_of_comments','-publish')[:5]
    most_disliked_posts = Post.objects.filter(status='published').order_by('-number_of_dislikes','-publish')[:5]
    if(request.method == 'POST'):
        username = request.POST.get('user')
        return HttpResponseRedirect(reverse('socialMedia:search',kwargs={'username':username}))
    return render(request,'homepage.html',{'user':request.user,'posts':posts,'newest_posts':newest_posts,'most_commented_posts':most_commented_posts,'most_disliked_posts':most_disliked_posts})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('socialMedia:user_login'))

@login_required
@isProfileCreated
def add_post(request):
    if(request.method == 'GET'):
        form = PostModelForm()
        return render(request,'addPost.html',{'form':form})
    
    
    if(request.method == 'POST'):
        form  = PostModelForm(request.POST)
        if(form.is_valid):
            title = request.POST.get('title')
            body = request.POST.get('body')
            post = Post(title=title,body=body,author=request.user.profile)
            if(request.FILES):
                picture = request.FILES.get('picture')
                post.picture = picture
                post.save()
                return HttpResponseRedirect(reverse('socialMedia:drafts'))
        return HttpResponseRedirect(reverse('socialMedia:add_post'))
        

@login_required
@isProfileCreated
def retrieve_drafts(request):
    posts = Post.objects.filter(author=request.user.profile,status='draft')
    return render(request,'drafts.html',{'posts':posts,'user':request.user})

@login_required
def publish(request,id):
    post = Post.objects.get(id=id)
    if(post.status == 'draft'):
        post.status = 'published'
        post.publish = timezone.now()
        post.save()
        everyPost = EveryPostByUser(title=post.title,author=request.user.profile,body=post.body)
        everyPost.save()
        follower = list(post.author.followers.all())
        follower_email = []
        for follow in follower:
            if(follow.user.email):
                follower_email.append(follow.user.email)
        if(len(follower_email)!= 0):        
            subject = f"{post.author.user.username} has made a new post"
            html_content = f"{post.author.user.username}  has made a new post with title {post.title}.To see the complete post click on the link http://127.0.0.1:8000/post/{post.id}"
            message = Mail(from_email='sarthak.intellify@gmail.com',to_emails=follower_email,subject=subject,html_content=html_content)
            try:
                sg = SendGridAPIClient(environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                 print(e.message)
    return HttpResponseRedirect(reverse('socialMedia:published'))

@login_required
def change_to_draft(request,id):
    post = Post.objects.get(id=id)
    if(post.status == 'published'):
        post.status = 'draft'
        post.publish = None
        post.save()
    return HttpResponseRedirect(reverse('socialMedia:drafts'))


@login_required
def retrieve_published(request):
    posts = Post.objects.filter(author=request.user.profile,status='published')
    author = request.user.profile
    return render(request,'published.html',{'posts':posts,'author':author,'user':request.user})

@login_required
def update(request,id):
    if(request.method == 'GET'):
        form = PostModelForm(instance=request.user.profile.post.get(id=id))
        return render(request,'update.html',{'form':form,'user':request.user})

    if(request.method == 'POST'):
        form  = PostModelForm(data=request.POST)
        if(form.is_valid):
            title = request.POST.get('title')
            body = request.POST.get('body')
            post = Post.objects.get(id=id)
            post.title = title
            post.body  = body
            post.save()
            if(post.status == 'published'):
                everyPost = EveryPostByUser(title=post.title,author=request.user.profile,body=post.body)
                everyPost.save()
            return HttpResponseRedirect(reverse('socialMedia:homepage'))
        return HttpResponseRedirect(reverse('socialMedia:update'))
        

@login_required
def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return HttpResponseRedirect(reverse('socialMedia:homepage'))

@login_required
def profile_data(request):
    if(request.method == 'GET'):
        user_form = UserProfileForm(instance=request.user)
        profile_form = ProfileModelForm(instance=request.user.profile)
        return render(request,'profile_data.html',{'user_form':user_form,'profile_form':profile_form,'user':request.user})
    
    if(request.method == 'POST'):
        user_form = UserProfileForm(data=request.POST)
        profile_form = ProfileModelForm(data=request.POST)
        if(user_form.is_valid and profile_form.is_valid):
            user = User.objects.get(id=request.user.id)
            profile = Profile.objects.get(user=request.user)
            user.first_name = request.POST.get('first_name') 
            user.last_name = request.POST.get('last_name') 
            user.email = request.POST.get('email')
            user.save()
            profile.github_account_url = request.POST.get('github_account_url')
            if(request.FILES):
                profile.profile_pic = request.FILES.get('profile_pic')
            profile.facebook_account_url = request.POST.get('facebook_account_url')
            profile.linkedIn_account_url = request.POST.get('linkedIn_account_url')
            profile.save()
            return HttpResponseRedirect(reverse('socialMedia:profile_data'))
        return HttpResponseRedirect(reverse('socialMedia:profile_data'))

@login_required
def see_complete_post(request, id):
    post = Post.objects.get(id=id)
    comments = post.post.filter(post=post)

    if(request.method=='POST'):
        comment = request.POST.get('comment')
        com_post = Comment(author=request.user.profile,comment=comment,post=post)
        post.number_of_comments += 1
        com_post.save()
        post.save()

    return render(request,'see_complete_post.html',{'post':post,'user':request.user,'comments':comments})

@login_required
def like(request,id):
    post = Post.objects.get(id=id)
    list_of_liker = post.likes
    list_of_disliker = post.dislikes
    number_of_likes = post.number_of_likes
    number_of_dislikes = post.number_of_dislikes
    print(list_of_liker)
    if(not list_of_liker.filter(id=request.user.profile.id)):
        if(list_of_disliker.filter(id=request.user.profile.id)):
            number_of_dislikes -= 1
            post.dislikes.remove(request.user.profile.id)
            post.number_of_dislikes =number_of_dislikes
        post.number_of_likes += 1
        post.likes.add(request.user.profile.id)
        post.save()
        return HttpResponseRedirect(reverse('socialMedia:complete_post',kwargs={'id':id}))
    return HttpResponseRedirect(reverse('socialMedia:complete_post',kwargs={'id':id}))


@login_required
def dislike(request,id):
    post = Post.objects.get(id=id)
    list_of_liker = post.likes
    list_of_disliker = post.dislikes
    number_of_likes = post.number_of_likes
    number_of_dislikes = post.number_of_dislikes
    print(list_of_liker)
    if(not list_of_disliker.filter(id=request.user.profile.id)):
        if(list_of_liker.filter(id=request.user.profile.id)):
            number_of_likes -= 1
            post.likes.remove(request.user.profile.id)
            post.number_of_likes =number_of_likes
        post.number_of_dislikes += 1
        post.dislikes.add(request.user.profile)
        post.save()
        return HttpResponseRedirect(reverse('socialMedia:complete_post',kwargs={'id':id}))
    return HttpResponseRedirect(reverse('socialMedia:complete_post',kwargs={'id':id}))

@login_required
def search(request,username):
    if(username == ''):
        return HttpResponseRedirect(reverse('socialMedia:homepage'))
    users = User.objects.filter(username__icontains=username) or User.objects.filter(first_name__icontains=username) or User.objects.filter(last_name__icontains=username)
    return render(request,'search.html',{'users':users})

@login_required
def get_user(request,id):
    user = User.objects.get(id=id)
    return render(request, 'getUser.html',{'user':user})

@login_required
def see_published_post(request,id):
    user = User.objects.get(id=id)
    isFollower = False
    isWantToBeFollower = False
    isNotFollower = False    
    if(user.profile.followers.filter(id = request.user.id)):
        isFollower = True
    elif(user.profile.want_to_be_follower.filter(id = request.user.id)):
        isWantToBeFollower = True
    else:
        isNotFollower = True
    
    posts = user.profile.post.all()
    return render(request,'see_published_post.html',{'user':user,'reqUser':request.user,'isFollower':isFollower,'isWantToBeFollower':isWantToBeFollower,'isNotFollower':isNotFollower,'posts':posts})

@login_required
def follower(request,id):
    user = User.objects.get(id=id)
    user.profile.want_to_be_follower.add(request.user.profile.id)
    user.profile.save()
    return HttpResponseRedirect(reverse('socialMedia:seePubPost',kwargs={'id':user.id}))

@login_required
def friend_request(request):
    friends = request.user.profile.want_to_be_follower.all()
    length = len(friends)
    return render(request,'friend_request.html',{'friends':friends,'length':length})

@login_required
def accept(request,id):
    profile = Profile.objects.get(id=id)
    profile.following.add(request.user.profile.id)
    request.user.profile.followers.add(id)
    request.user.profile.want_to_be_follower.remove(id)
    profile.save()
    request.user.profile.save()
    return HttpResponseRedirect(reverse('socialMedia:friend_request'))
 

@login_required
def reject(request,id):
    request.user.profile.want_to_be_follower.remove(id)
    request.user.profile.save()
    return HttpResponseRedirect(reverse('socialMedia:friend_request'))

@login_required
def list_of_follower(request):
    followers = request.user.profile.followers.all()
    return render(request,'list_of_follower.html',{'followers':followers})

@login_required
def following(request):
    followings = request.user.profile.following.all()
    return render(request,'list_of_following.html',{'followings':followings})

def news_feed(request):
    news = []
    for post in Post.objects.filter(status='published').order_by('-publish'):
        if(request.user.profile.following.filter(id=post.author.id)):
            news.append(post)
    length2 = len(news)
    return render(request,'news_feed.html',{'post':news,'length2':length2})

class passwordChangeView(PasswordChangeView):
    success_url = reverse_lazy('socialMedia:password_change_done')