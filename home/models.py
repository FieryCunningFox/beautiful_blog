from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.text import slugify
import string, random

def generate_random_string(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))


def generate_slug(text):
    new_slug = slugify(text)
    if blogModel.objects.filter(slug = new_slug).exists():
        generate_slug(text + generate_random_string(5))
    return new_slug


class AuthorProfile(models.Model):
    
    class Meta:
        verbose_name_plural = "Authors"
        
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")

    bio = models.TextField()
    instagram = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.__class__.__name__} object for {self.user}"
    

class Tag(models.Model):
    class Meta:
        verbose_name_plural = "Tags"
        
    value = models.TextField(max_length=100)

    def __str__(self):
        return self.value


class Comment(models.Model):
    class Meta:
        verbose_name_plural = "Comments"
        
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content[:30]} ..."


class blogModel(models.Model):
    
    class Meta:
        verbose_name_plural = "Posts"
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=300)
    content = FroalaField()
    summary = models.TextField(max_length=500, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="posts")
    comments = GenericRelation(Comment)
    slug = models.SlugField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to="blog", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True, db_index=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(blogModel, self).save(*args, **kwargs)
        

