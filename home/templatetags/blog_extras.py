from django.contrib.auth import get_user_model
from django import template
from django.utils import timezone
from django.utils.html import (
    format_html,
)  # escapes strings parameters before interpolation

# from .models import blogModel
from django.contrib.auth.models import User
from django.conf import settings
from datetime import timedelta

import logging

logger = logging.getLogger(__name__)

user_model = get_user_model()
register = template.Library()

User.objects.filter(
    is_active=False,
    date_joined=timezone.now() - timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS),
).delete()


@register.filter
def author_details(author, current_user=None):
    if not isinstance(author, user_model):
        return ""  # return empty string as safe default

    if author == current_user:
        return format_html("<strong>me</strong>")

    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"

    suffix = ""
    # prefix = format_html('<a href="mailto:{}">', author.email)
    # suffix = format_html("</a>")
    prefix = ""
    return format_html("{}{}{}", prefix, name, suffix)


# @register.inclusion_tag("blog/post-list.html")
# def resent_posts(post):  # get 5 resent posts
#     posts = Post.objects.filter(published_at__lte=timezone.now())[:5]
#     logger.debug("Loaded %d recent posts for post %d", len(posts), post.pk)
#     return {'title': 'Recent Posts', 'posts': posts}


@register.simple_tag
def row(extra_classes=""):
    return format_html('<div class="row {}">', extra_classes)


@register.simple_tag
def end():
    return format_html("</div>")


@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}"', extra_classes)
