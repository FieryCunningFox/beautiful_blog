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

from .models import blogModel
from .forms import CommentForm,  EmailPostForm


def home(request):
    context = {}
    posts = (
        blogModel.objects.filter(published_at__lte=timezone.now())
        .select_related("author")
        .defer('created_at', 'modified_at')
    )
    
    current_page = Paginator(posts, 10)
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

def post_share(request, slug):  
    post = get_object_or_404(blogModel, slug=slug)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"""{cd['name']} ({cd['email']}) recommends you reading " {post.title}\""""
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:  
        form = EmailPostForm()
    return render(request, 'share.html', {'post': post, 'form': form, 'sent': sent})
    

class author_profile(TemplateView):
    template_name = "author.html"


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