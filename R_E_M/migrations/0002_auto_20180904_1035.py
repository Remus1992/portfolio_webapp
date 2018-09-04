# Generated by Django 2.0.6 on 2018-09-04 17:35

from django.db import migrations, models
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('R_E_M', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', martor.models.MartorField()),
            ],
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=martor.models.MartorField(),
        ),
    ]
