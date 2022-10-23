from django.contrib import admin
from django.contrib.auth.models import User
from .models import blogModel, NewsModel, Tag, Comment, AuthorProfile, Question


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class TagSearch(admin.ModelAdmin):
    list_display = ("value", )


admin.site.register(blogModel)
admin.site.register(NewsModel)
# admin.site.register(User, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(AuthorProfile)
admin.site.register(Question)
