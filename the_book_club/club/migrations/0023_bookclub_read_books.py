# Generated by Django 4.2 on 2023-05-24 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0022_remove_clubpage_book_club_remove_bookclub_book_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookclub',
            name='read_books',
            field=models.ManyToManyField(related_name='read_clubs', to='club.book'),
        ),
    ]