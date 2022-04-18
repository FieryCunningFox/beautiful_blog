from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class TagSearch(admin.ModelAdmin):
    list_display = ("value", )


admin.site.register(blogModel)
# admin.site.register(, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(AuthorProfile)

