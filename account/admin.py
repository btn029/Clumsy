from django.contrib import admin

from .models import Employee, Post, Comment
admin.site.register(Employee)
admin.site.register(Post)
admin.site.register(Comment)