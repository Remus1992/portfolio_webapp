# Generated by Django 2.0.6 on 2018-09-29 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('R_E_M', '0004_album_album_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='date',
            field=models.CharField(max_length=50),
        ),
    ]