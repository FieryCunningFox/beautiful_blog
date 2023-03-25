from django.contrib import admin
from home.models import Post, NewsModel, Tag, Comment, Question


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class TagSearch(admin.ModelAdmin):
    list_display = ("value",)


admin.site.register(Post)
admin.site.register(NewsModel)
admin.site.register(Tag)
admin.site.register(Comment)
# admin.site.register(AuthorProfile)
admin.site.register(Question)
