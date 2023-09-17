from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .filters import CommentsFilter
from .models import Post, Comment
from .forms import PostForm, CommentForm, RegisterForm

from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

from .token import account_activation_token

from django.core.mail import EmailMessage


class PostList(ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    ordering = ['-id']
    paginate_by = 5


class PostDetail(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'posts/post_create.html'
    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'posts/post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'posts/post_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('board:posts')


class CommentList(ListView):
    model = Comment
    template_name = 'posts/comments.html'
    context_object_name = 'comments'
    queryset = Comment.objects.order_by('-id')
    ordering = ['-id']
    paginate_by = 5

    def get_queryset(self):
        return Comment.objects.filter(commentPost__author__authorUser=self.request.user).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CommentsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CommentDetail(DetailView):
    model = Comment
    template_name = 'posts/comment.html'
    context_object_name = 'comment'


class CommentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'posts/comment_create.html'
    form_class = CommentForm
    success_url = reverse_lazy('board:posts')


@login_required
def accept_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if not comment.is_accepted:
        comment.accept()
    return redirect('board:comments')


@login_required
def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()
    return redirect('board:comments')


class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'posts/user.html'


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'posts/signup.html'
    success_url = '/'


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('mail/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = RegisterForm()
    return render(request, 'posts/signup.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
