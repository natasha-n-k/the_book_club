# Generated by Django 4.2 on 2023-05-26 18:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('club', '0023_bookclub_read_books'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookclub',
            name='book_queue_members',
            field=models.ManyToManyField(related_name='queued_books', through='club.Queue', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='queue',
            name='book',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='club.book'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='queue',
            name='member',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
