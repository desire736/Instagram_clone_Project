import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.views.generic.base import TemplateView, View
from django.db.models import Count
from .forms import CommentForm

from instagram_core.models import Publication, GaleryImage, Like, PublicationComment
from users.models import CustomFollow, CustomUser


class ProfileView(DetailView):
    model = CustomUser
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.get_object()
        current_user = self.request.user

        is_own_profile = user == current_user

        publications = Publication.objects.filter(user=user)
        followers_count = CustomFollow.objects.filter(following=user).count()
        following_count = CustomFollow.objects.filter(follower=user).count()
        post_count = publications.count()

        publication_images = []
        for pub in publications:
            first_image = pub.images.first()
            if first_image:
                publication_images.append(first_image.image.url)

        context.update({
            'user': user,
            'avatar_image': user.avatar_image.url if user.avatar_image else None,
            'followers_count': followers_count,
            'following_count': following_count,
            'post_count': post_count,
            'publication_images': publication_images,
            'is_own_profile': is_own_profile,
        })

        return context

class HomeView(TemplateView):
    """Вью для домашней страницы"""
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            followers = CustomFollow.objects.filter(following=user).select_related('follower')
            following = CustomFollow.objects.filter(follower=user).select_related('following')
            user_ava = self.request.user

            following_users = [follow.following for follow in following]

            publications = (
                Publication.objects
                .select_related("user")
                .prefetch_related("likes", "comments", "images")
                .filter(user__in=following_users)
                .order_by("-created_at")
            )
            for publication in publications:
                publication.user_likes = user in publication.likes.all()
                publication.images_list = [image.image.url for image in publication.images.all()]

            context = {
                "followers": [follow.follower for follow in followers],
                "following": following_users,
                "publications": publications,
                'avatar_image': user.avatar_image.url,
            }
            return render(request, self.template_name, context)

        return redirect("login")


class ReelsView(TemplateView):
    template_name = 'reels.html'

    def get_context_data(self,  *args , **kwargs):
        user = self.request.user

        context = {
            'user': user,
            'avatar_image': user.avatar_image.url
        }
        return context

class ExploreView(TemplateView):
    template_name = 'explore.html'

    def get_context_data(self,  *args , **kwargs):
        user = self.request.user

        context = {
            'user': user,
            'avatar_image': user.avatar_image.url
        }
        return context

class NotificationView(TemplateView):
    template_name = 'notification.html'

    def get_context_data(self,  *args , **kwargs):
        user = self.request.user

        context = {
            'user': user,
            'avatar_image': user.avatar_image.url
        }
        return context


class CreateNewPostView(View):
    def post(self, request, *args, **kwargs):
        current_user = request.user  # Текущий пользователь
        data = request.POST  # Данные формы
        files = request.FILES.getlist('image-upload')  # Список загруженных изображений

        # Создаем объект Publication
        new_publication = Publication.objects.create(
            user=current_user,
            descriptions=data.get('description', '')  # Описание
        )

        # Создаем записи GaleryImage для каждого изображения
        for image_file in files:
            GaleryImage.objects.create(
                post=new_publication,  # Связь с публикацией
                image=image_file       # Изображение
            )

        return redirect('home')


class LikeToggleView(View):
    """Вьюшка для добавления/удаления лайка"""

    def post(self, request, *args, **kwargs):
        user = request.user
        publication_id = kwargs['pk']
        publication = get_object_or_404(Publication, pk=publication_id)

        like_exists = Like.objects.filter(user=user, publication=publication).exists()

        if like_exists:
            Like.objects.filter(user=user, publication=publication).delete()
            action = 'unliked'
        else:
            Like.objects.create(user=user, publication=publication)
            action = 'liked'

        return JsonResponse({'success': True, 'action': action, 'likes_count': publication.likes.count()})

class AddCommentView(View):
    """Вьюшка для добавления комментариев и отображения комментариев на странице публикации"""

    def get(self, request, *args, **kwargs):
        try:
            publication = Publication.objects.get(id=kwargs['pk'])
        except Publication.DoesNotExist:
            return redirect('home')  # Если публикации нет, редиректим на главную

        comments = PublicationComment.objects.filter(publication=publication)

        context = {
            'publication': publication,
            'comments': comments,  # передаем комментарии в контекст
            'form': CommentForm(),
        }

        return redirect(request.path)

    def post(self, request, *args, **kwargs):
        user = request.user
        text = request.POST.get('comment')

        if not text:
            return JsonResponse({"success": False, "error": "Comment cannot be empty"})

        try:
            publication = Publication.objects.get(id=kwargs['pk'])
        except Publication.DoesNotExist:
            return JsonResponse({"success": False, "error": "Publication not found"})

        # Создание комментария
        comment = PublicationComment.objects.create(author=user, publication=publication, text=text)

        # После создания комментария, редиректим обратно на страницу публикации
        return redirect(request.get_full_path())

class PublicationDetailView(DetailView):
    model = Publication
    context_object_name = 'publication'
    template_name = 'home.html'  # Указываем шаблон, который хотите использовать

    def get_object(self, queryset=None):
        # Получаем объект публикации по ID, переданному в URL
        return get_object_or_404(Publication, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем публикацию
        publication = context['publication']

        # Список комментариев
        comments = PublicationComment.objects.filter(publication=publication)

        # Добавляем комментарии в контекст
        context['comments'] = comments

        return context

class LikedView(View):
    """Вьюшка для того, чтобы ставить лайки и снимать их"""

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            publication = Publication.objects.get(id=kwargs['pk'])
        except Publication.DoesNotExist:
            return JsonResponse({"success": False, "error": "Publication not found"})

        like, created = Like.objects.get_or_create(user=user, publication=publication)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return JsonResponse({"success": True, "liked": liked})