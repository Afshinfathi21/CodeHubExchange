# Generated by Django 4.2.6 on 2024-01-07 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0010_alter_comment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
