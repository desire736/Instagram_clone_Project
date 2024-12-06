from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.views.generic.base import TemplateView, View
from django.contrib.auth import login, logout
from pyexpat.errors import messages
from django.http import JsonResponse
from .models import CustomUser, CustomFollow

class RegisterView(TemplateView):
    template_name = 'sign_up.html'

class MakeRegisterView(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        password = data['password']

        user = CustomUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,

        )
        user.save()
        login(request, user)
        return redirect('profile', pk=request.user.pk)

class LoginerView(TemplateView):
    template_name = 'login.html'

class MakeLoginerView(View):
    def post(self, request, *args,  **kwargs):
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            messages.error(request, "Пользователь не существует.")
            return redirect('login')

        if user.check_password(password):
            login(request, user)
            return redirect('profile', pk=user.pk)
        else:
            return redirect('login')

class MakeLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)  # Завершаем сессию пользователя
        return redirect('login')

class MessagesView(TemplateView):
    template_name = 'messages.html'

    def get_context_data(self,  *args , **kwargs):
        user = self.request.user

        context = {
            'user': user,
            'avatar_image': user.avatar_image.url
        }
        return context

class MakeFollowView(View):
    """Вьюшка для подписки/отписки на пользователя"""

    def post(self, request, *args, **kwargs):
        user = request.user  # Текущий пользователь
        follow_user_id = kwargs.get('pk')  # ID пользователя, на которого подписываемся

        try:
            follow_user = CustomUser.objects.get(id=follow_user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({"success": False, "error": "Пользователь не найден"})

        if user == follow_user:
            return JsonResponse({"success": False, "error": "Нельзя подписаться на самого себя"})

        # Проверяем наличие существующей подписки
        existing_follow = CustomFollow.objects.filter(follower=user, following=follow_user).first()

        if existing_follow:
            # Если подписка существует, удаляем (отписка)
            existing_follow.delete()
            action = 'unfollowed'
        else:
            # Если подписки нет, создаём новую (подписка)
            CustomFollow.objects.create(follower=user, following=follow_user)
            action = 'followed'

        return JsonResponse({'success': True, 'action': action})

