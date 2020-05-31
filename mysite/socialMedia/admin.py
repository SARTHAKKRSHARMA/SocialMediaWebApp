from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user',)
    raw_id_fields = ('user',)

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('author','status')
    raw_id_fields = ('author',)

@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('post','author','created')
    raw_id_fields = ('post','author')

@admin.register(EveryPostByUser)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('author','publish')
    raw_id_fields = ('author',)
    search_fields = ('title','body')
