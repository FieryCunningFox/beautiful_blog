from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from .helpers import *


class blogModel(models.Model):
    title = models.CharField(max_length=300)
    content = FroalaField()
    slug = models.SlugField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to="blog")
    created_at = models.DateTimeField(auto_now_add=True)
    upload_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(blogModel, self).save(*args, **kwargs)
        