from django.utils.text import slugify
from home.models import *

import string, random

def generate_random_string(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))


def generate_slug(text):
    new_slug = slugify(text)
    if blogModel.objects.filter(slug = new_slug).exists():
        generate_slug(text + generate_random_string(5))
    return new_slug