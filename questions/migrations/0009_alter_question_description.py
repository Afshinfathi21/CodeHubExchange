# Generated by Django 4.2.6 on 2024-01-06 09:15

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_comment_is_answer_delete_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
