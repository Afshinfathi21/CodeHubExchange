# Generated by Django 4.2.6 on 2023-12-16 12:29

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_remove_vote_vote_type_vote_vote_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=tinymce.models.HTMLField(),
        ),
    ]
