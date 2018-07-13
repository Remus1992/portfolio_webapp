# Generated by Django 2.0.6 on 2018-07-13 19:18

import R_E_M.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('R_E_M', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieStillPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=R_E_M.models.photo_image_uh)),
                ('alt_text', models.CharField(blank=True, max_length=50, null=True)),
                ('date_taken', models.CharField(max_length=50)),
                ('image_details', models.TextField()),
                ('movie_album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_photo_album', to='R_E_M.Movie')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_photos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
