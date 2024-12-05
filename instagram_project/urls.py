"""
URL configuration for instagram_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from instagram_core import views

from instagram_core.views import ProfileView, HomeView, ReelsView, ExploreView, NotificationView, CreateNewPostView, \
    LikeToggleView, AddCommentView, LikedView
from django.conf import settings
from django.conf.urls.static import static
from users.views import RegisterView, LoginerView, MakeRegisterView, MakeLoginerView, MakeLogoutView, MessagesView, \
    MakeFollowView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', RegisterView.as_view(), name='register'),
    path('make/registration/', MakeRegisterView.as_view(), name='make_register'),
    path('login/', LoginerView.as_view(), name='login'),
    path('make/login/', MakeLoginerView.as_view(), name='make_login'),
    path('make/logout/', MakeLogoutView.as_view(), name='make_logout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('home/', HomeView.as_view(), name='home'),
    path('reels/', ReelsView.as_view(), name='reels'),
    path('messages/', MessagesView.as_view(), name='messages'),
    path('explore/', ExploreView.as_view(), name='explore'),
    path('notification/', NotificationView.as_view(), name='notification'),
    path('create-new-post/', CreateNewPostView.as_view(), name='create-new-post-url'),
    path('follow/<int:pk>/', MakeFollowView.as_view(), name='make-follow-url'),
    path('like/<int:pk>/', LikeToggleView.as_view(), name='like-toggle'),
    path('add_comment/<int:pk>/', AddCommentView.as_view(), name='add-comment'),
    path('publication/<int:pk>/', views.PublicationDetailView.as_view(), name='publication_detail'),
    path('toggle-like/<int:pk>/', LikedView.as_view(), name='toggle_like'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
