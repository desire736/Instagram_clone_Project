# Generated by Django 5.1.3 on 2024-11-26 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_publications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar_image',
            field=models.ImageField(blank=True, default='images/profile.jpg', null=True, upload_to=''),
        ),
    ]