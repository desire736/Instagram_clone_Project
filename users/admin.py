from django.contrib import admin

from instagram_core.models import Publication
from users.models import CustomUser, CustomFollow


from users.models import CustomFollow, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username']
    model = CustomUser
    inlines = []

    def publications_list(self, obj):
        return ", ".join([publication.title for publication in obj.publications.all()])
    publications_list.short_description = "Публикации"

    list_display = ['username', 'publications_list']

@admin.register(CustomFollow)
class CustomUserFollowerAdmin(admin.ModelAdmin):
    list_display = ['following', 'follower']