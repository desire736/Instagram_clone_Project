# Generated by Django 5.1.3 on 2024-12-04 17:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram_core', '0004_publication_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='like',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
