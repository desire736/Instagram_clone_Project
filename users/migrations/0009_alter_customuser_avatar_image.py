# Generated by Django 5.1.3 on 2024-12-01 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_customuser_avatar_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar_image',
            field=models.ImageField(blank=True, default='assets/images/profile_img.jpg', null=True, upload_to=''),
        ),
    ]