from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.text import slugify
import string, random


def generate_random_string(n: int):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=n))


def generate_slug(text):
    new_slug = slugify(text)
    if Post.objects.filter(slug=new_slug).exists():
        generate_slug(text + generate_random_string(5))
    return new_slug


# class AuthorProfile(models.Model):
#     class Meta:
#         verbose_name_plural = "Authors"

#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, null=True, related_name="profile"
#     )
#     bio = models.TextField()
#     instagram = models.CharField(max_length=50, null=True, blank=True)

#     def __str__(self):
#         return f"{self.__class__.__name__} object for {self.user}"


class Tag(models.Model):
    class Meta:
        verbose_name_plural = "Tags"

    value = models.TextField(max_length=100)

    def __str__(self):
        return self.value


class Comment(models.Model):
    class Meta:
        verbose_name_plural = "Comments"

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300, verbose_name="")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content[:30]} ..."


class Question(models.Model):
    class Meta:
        verbose_name_plural = "Questions"

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField(max_length=300)

    def __str__(self):
        return f"{self.message[:30]} ..."

    def save(self, *args, **kwargs):
        super(Question, self).save(*args, **kwargs)


class Post(models.Model):
    class Meta:
        verbose_name_plural = "Posts"

    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    content = FroalaField(
        options={
            "toolbarInline": True,
        }
    )
    summary = models.TextField(max_length=500, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="posts")
    comments = GenericRelation(Comment)
    slug = models.SlugField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to="blog", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True, db_index=True)

    # all_tags = TaggableManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/posts/{self.slug}"


class NewsModel(models.Model):
    class Meta:
        verbose_name_plural = "News"

    title = models.CharField(max_length=300, blank=True, null=True)
    summary = models.CharField(max_length=600, blank=True, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to="blog", blank=True, null=True)
    comments = GenericRelation(Comment)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    published_at = models.CharField(max_length=300, null=True, blank=True)
    link = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(NewsModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/news{self.sluf}"
