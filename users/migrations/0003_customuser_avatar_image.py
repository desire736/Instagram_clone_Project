# Generated by Django 5.1.3 on 2024-11-25 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='avatar_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
