from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.utils import timezone

from .models import blogModel
from .forms import CommentForm


def home(request):
    posts = (
        blogModel.objects.filter(published_at__lte=timezone.now())
        .select_related("author")
        .defer('created_at', 'modified_at')
    )  # only that post already published
    return render(request, 'home.html', {"posts": posts})
# upload_date__lte=timezone.now()

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def posts(request, slug):
    post = get_object_or_404(blogModel, slug=slug)

    if request.user.is_authenticated:  # check if the user is active
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    return render(request, 'posts.html', {"post": post, "comment_form": comment_form})

def register(request):
    return render(request, 'register.html')

class LoginView(TemplateView):
    template_name = "login.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                context['error'] = "Wrong username or password"
        return render(request, self.template_name, context)