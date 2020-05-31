import os
from django.conf import settings
from django.contrib import admin
from openpyxl import Workbook
from openpyxl import load_workbook
from django.utils import timezone
from .models import *
# Register your models here.
def generate_stat(Modeladmin, request, queryset):
    filepath = os.path.join(settings.BASE_DIR,'data.xlsx')
    data = load_workbook(filepath)
    sheet = data.active
    empty_row = ("","","","","","","")
    row1 = ("","","DATA Generated On",str(timezone.now()))
    row2 = ("Username","Name","Number_of_followers","Following","PostCount")
    sheet.append(empty_row)
    sheet.append(empty_row)
    sheet.append(row1)
    sheet.append(row2)
    for profile in queryset:
        username = profile.user.username
        name = profile.user.first_name
        follower_count = profile.followers.all().count()
        following_count = profile.following.all().count()
        post_count = profile.post.all().count()

        data_row = (username,name,follower_count,following_count,post_count)
        sheet.append(data_row)
        data.save(filepath)
    


class DataAdmin(admin.ModelAdmin):
    actions = [generate_stat,]

admin.site.register(Profile,DataAdmin)

# @admin.register(Profile)
# class ProfileModelAdmin(admin.ModelAdmin):
#     list_display = ('user',)
#     raw_id_fields = ('user',)

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
