# Generated by Django 4.2 on 2023-05-19 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0015_alter_book_average_rating_alter_rating_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbook',
            name='average_rating',
        ),
    ]
