from django.contrib import admin
from blogging.models import Post, PostAdmin
from blogging.models import Category, CategoryAdmin

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
