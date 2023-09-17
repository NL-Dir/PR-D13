from django.urls import path
from .views import PostList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView, CommentList, CommentDetail, \
    CommentCreateView, accept_comment, delete_comment, UserView, RegisterView, activate, signup
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'board'

urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/edit/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('post/comments', CommentList.as_view(), name='comments'),
    path('post/comment/<int:pk>', CommentDetail.as_view(), name='comment'),
    path('post/comment_create', CommentCreateView.as_view(), name='comment_create'),
    path('post/comment/<int:pk>/accept', accept_comment, name='accept'),
    path('post/comment/<int:pk>/delete', delete_comment, name='delete'),
    path('user', UserView.as_view(), name='user'),
    path('login/', LoginView.as_view(template_name='posts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='posts/logout.html'), name='logout'),
    path('signup/', signup , name='signup'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
