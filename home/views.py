from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic import TemplateView
from django.utils import timezone

from .models import blogModel, AuthorProfile, NewsModel
from .forms import CommentForm,  EmailPostForm, FormProfile, QuestionForm, blogForm
# from taggit.models import Tag
import time


def home(request):
    context = {}
    posts = (
        blogModel.objects.filter(published_at__lte=timezone.now())
        .select_related("author")
        .defer('created_at', 'modified_at')
    )
    current_page = Paginator(posts, 7)
    page = request.GET.get('page')
    try:  
        context['posts'] = current_page.page(page)  
    except PageNotAnInteger:
        context['posts'] = current_page.page(1)  
    except EmptyPage:
        context['posts'] = current_page.page(current_page.num_pages)
        
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            question_form = QuestionForm(request.POST)
            
            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.creator = request.user
                question.save()
                return redirect(request.path_info)
        else:
            question_form = QuestionForm()
    else:
        if request.method == 'POST':
            question_form = QuestionForm(request.POST)
            
            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.creator = request.user
                question.save()
                return redirect(request.path_info)
        else:
            question_form = QuestionForm()
            
    return render(request, 'contact.html', {'question_form': question_form, })


def posts(request, slug, tag_slug=None):
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


def search_posts(request, tag_slug):
    context = {}
    posts = (
        blogModel.objects.filter(published_at__lte=timezone.now())
        .select_related("author")
        .defer('created_at', 'modified_at')
    )
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = posts.filter(all_tags__in=[tag])
    
    current_page = Paginator(posts, 7)
    page = request.GET.get('page')
    try:  
        context['posts'] = current_page.page(page)  
    except PageNotAnInteger:
        context['posts'] = current_page.page(1)  
    except EmptyPage:
        context['posts'] = current_page.page(current_page.num_pages)
    context['tag'] = tag
        
    return render(request, 'posts_tag_list.html', context)


def post_share(request, slug):  
    post = get_object_or_404(blogModel, slug=slug, published_at__lte=timezone.now())
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"""{cd['name']} ({cd['email']}) recommends you reading "{post.title}\""""
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'svetl.rudnewa2014@yandex.ru', [cd['to']])
            sent = True
    else:  
        form = EmailPostForm()
    return render(request, 'share.html', {"post": post, "form": form, "sent": sent})
    

def author_profile(request):
    posts = (
        blogModel.objects.filter(author=request.user)
        .defer('created_at', 'modified_at')
    )
    
    return render(request, "author.html", {"posts":posts})


def profile_information(request):
    user = request.user
    person = get_object_or_404(AuthorProfile, user=user)
    if person is None:
        if request.method == 'POST':
            profile_form = FormProfile(request.POST)

            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                return redirect(request.path_info)
        else:
            profile_form = FormProfile()
    else:
        if request.method == 'POST':
            profile_form = FormProfile(request.POST)
            if profile_form.is_valid():
                person.bio = request.POST["bio"]
                if request.POST["instagram"]:
                    person.instagram = request.POST["instagram"]
                person.save()
                return redirect(request.path_info)
            
        else:
            profile_form = FormProfile(instance=person)
    
    return render(request, "profile_information.html", {"profile_form": profile_form})

def edit_and_publish(request, slug):
    author = request.user
    post = get_object_or_404(blogModel, author=author, slug=slug)
    if request.method == 'POST':
        edit_form = blogForm(request.POST)
        if edit_form.is_valid():
            post.title = request.POST['title']
            post.summary = request.POST['summary']
            post.content = request.POST['content']
            post.all_tags = request.POST['tags']
            post.image = request.POST['image']
            post.published_at = request.POST['published_at']
            post.save()
            return redirect("profile/")
    else:
        edit_form = blogForm(instance=post)
    return render(request, "add_new_post.html", {"blog_form": edit_form})
    
    
def about_author(request, username):
    user = get_object_or_404(User, username=username)
    author = AuthorProfile.objects.filter(user=user)
    if author is None:
        author = user
    posts = (
        blogModel.objects.filter(published_at__lte=timezone.now(), author=user)
        .select_related("author")
        .defer('created_at', 'modified_at')
    )
    current_page = Paginator(posts, 7)
    page = request.GET.get('page')
    try:  
        posts = current_page.page(page)  
    except PageNotAnInteger:
        posts = current_page.page(1)  
    except EmptyPage:
        posts = current_page.page(current_page.num_pages)
    return render(request, "about_author.html", {"author": author, "posts": posts, "user": user})


def add_new_post(request):
    if request.method == 'POST':
        blog_form = blogForm(request.POST)
        
        if blog_form.is_valid():
            article = blog_form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect(request.path_info)
    else:
        blog_form = blogForm()
    return render(request, "add_new_post.html", {"blog_form": blog_form})


def news_from_parser(request):
    posts = (
            NewsModel.objects.all()
        )
    number = 20
    current_page = Paginator(posts, 7)
    page = request.GET.get('page')
    context = {}
    try:  
        context['posts'] = current_page.page(page)  
    except PageNotAnInteger:
        context['posts'] = current_page.page(1)  
    except EmptyPage:
        context['posts'] = current_page.page(current_page.num_pages)
        
    context['number'] = number
    return render(request, "news.html", context)


def news_details(request, slug):
    post = get_object_or_404(NewsModel, slug=slug)

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
    return render(request, 'news_details.html', {"post": post, "comment_form": comment_form})
    
class LoginView(TemplateView):
    form_class = AuthenticationForm
    template_name = "login.html"
    
    success_url = "/"
    
    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['login_username']
            password = request.POST['login_password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile")
            else:
                context['error'] = "Wrong username or password"
        return render(request, self.template_name, context)
    

class RegisterView(TemplateView):
    form_class = UserCreationForm
    template_name = "register.html"
    
    success_url = "/"
    
    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['register_username']
            email = request.POST['register_email']
            password1 = request.POST['register_password']
            password2 = request.POST['register_repeat_password']
            
            if password1 == password2:
                User.objects.create_user(username, email, password1)
                return redirect(reverse("login"))
            else:
                context['error'] = "Something wrong, please try again"
        return render(request, self.template_name, context)


class LogoutView(TemplateView):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")