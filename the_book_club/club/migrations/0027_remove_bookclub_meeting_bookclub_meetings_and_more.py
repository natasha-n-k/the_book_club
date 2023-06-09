# Generated by Django 4.2 on 2023-06-01 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0026_bookclub_book_queue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookclub',
            name='meeting',
        ),
        migrations.AddField(
            model_name='bookclub',
            name='meetings',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='club_meeting', to='club.meeting'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='club',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='club_meeting', to='club.bookclub'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meeting',
            name='location_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
