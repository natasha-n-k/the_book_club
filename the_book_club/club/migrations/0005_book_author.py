# Generated by Django 4.2 on 2023-05-09 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0004_bookclub_venue'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(default='None', max_length=200, null=True),
        ),
    ]