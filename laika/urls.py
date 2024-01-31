from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    AboutView,
    PostListView, 
    PostCreateView, 
    PostUpdateView, 
    PostDetailView, 
    PostDeleteView, 
    LaikaProfileView,
    LaikaProfileListView,
    LaikaProfileCreateView,
    LaikaProfileDetailView,
    LaikaProfileUpdateView,
    LaikaProfileDeleteView,
    FollowUserView,
    UnfollowUserView,
    SendMessageView, 
    InboxView
)

urlpatterns = [
    path('posts/', PostListView.as_view(), name='laika-post-list'),
    path('create/', PostCreateView.as_view(), name='laika-post-create'),
    path('<int:pk>/', PostDetailView.as_view(), name='laika-post-detail'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='laika-post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='laika-post-delete'),
    
    path('profile/', LaikaProfileView.as_view(), name='laika-profile'),
    path('', LaikaProfileListView.as_view(), name='laika-profile-list'),
    path('profile/<int:pk>/', LaikaProfileDetailView.as_view(), name='laika-profile-detail'),
    path('profile/<int:pk>/edit/', LaikaProfileUpdateView.as_view(), name='laika-profile-edit'),
    path('profile/<int:pk>/delete/', LaikaProfileDeleteView.as_view(), name='laika-profile-delete'),
    
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    
    path('send-message/<int:user_id>/', SendMessageView.as_view(), name='send-message'),
    path('inbox/', InboxView.as_view(), name='messages'),

] 


