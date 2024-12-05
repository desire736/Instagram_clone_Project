from django.db import models

from users.models import CustomUser


class Publication(models.Model):
    user = models.ForeignKey(CustomUser, related_name='publications', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=150)
    descriptions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title

class GaleryImage(models.Model):
    post = models.ForeignKey(Publication, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Галерея изображений, для {self.post.title}'

class Like(models.Model):
    user = models.ForeignKey(CustomUser, related_name="likes", on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'publication')

    def __str__(self):
        return f'{self.user.username} likes {self.publication.title}'

class PublicationComment(models.Model):
    """Моделька для комментариев"""

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.TextField()
    updated_at = models.TextField()