# Generated by Django 4.2 on 2023-05-22 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('club', '0016_remove_userbook_average_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookclub',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='administered_clubs', to=settings.AUTH_USER_MODEL),
        ),
    ]
