from django.db import models
from django.contrib.auth.admin import User
from django.utils import timezone
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    github_account_url = models.URLField(blank=True,null=True)
    facebook_account_url = models.URLField(blank=True,null=True)
    linkedIn_account_url = models.URLField(blank=True,null=True)
    profile_pic = models.ImageField(upload_to = 'profilePic/%Y/%m/%d/',blank=True,null=True)
    following = models.ManyToManyField('Profile',related_name='followings',blank=True)
    followers = models.ManyToManyField('Profile',related_name='follower',blank=True)
    want_to_be_follower = models.ManyToManyField('Profile',related_name='wants_to_be_follower',blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    choice = (
        ('draft','Draft'),
        ('published','Published')
    )
    title = models.CharField(max_length = 300)
    author = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='post')
    body = models.TextField(blank=True)
    picture = models.ImageField(upload_to='post/%Y/%m/%d/',blank=True,null=True)
    created = models.DateTimeField(default = timezone.now)
    publish = models.DateTimeField(blank=True,null=True)
    status = models.CharField(max_length=9,choices=choice,default='draft')
    likes = models.ManyToManyField('Profile',related_name='likers',blank=True)
    number_of_likes = models.IntegerField(default=0)
    number_of_dislikes = models.IntegerField(default=0)
    number_of_comments = models.IntegerField(default=0)
    dislikes = models.ManyToManyField('Profile',related_name='disliker',blank=True)
    

    def __str__(self):
        return self.title

class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post',blank=True,null=True)
    author = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='comment',blank=True,null=True)
    created = models.DateTimeField(default=timezone.now)

class EveryPostByUser(models.Model):
    title = models.CharField(max_length = 300)
    author = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='everyPost')
    body = models.TextField(blank=True)
    publish = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return self.title
