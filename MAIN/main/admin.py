from django.contrib import admin

# inregistrarea modelelor
from .models import Category, Author, Post, Comment, Reply

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)


