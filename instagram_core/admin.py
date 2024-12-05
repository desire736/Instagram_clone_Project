from django.contrib import admin

from instagram_core.models import Publication, GaleryImage, Like
from instagram_core.views import AddCommentView

class PublicationImageInline(admin.TabularInline):
    model = GaleryImage
    extra = 1
class PostAdmin(admin.ModelAdmin):
    inlines = [PublicationImageInline]
class LikedAdmin(admin.ModelAdmin):
    model = Like

admin.site.register(Publication, PostAdmin)
admin.site.register(Like, LikedAdmin)
