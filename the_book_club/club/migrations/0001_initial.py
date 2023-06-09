# Generated by Django 4.2 on 2023-05-05 17:56

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('language', models.CharField(max_length=2)),
                ('image', models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='media'), upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='BookClub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('language', models.CharField(max_length=2)),
                ('image', models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='media'), upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='ClubPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('language', models.CharField(max_length=2)),
                ('book_club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.bookclub')),
            ],
        ),
        migrations.CreateModel(
            name='BookPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('language', models.CharField(max_length=2)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.bookclub')),
            ],
        ),
    ]
