# Generated by Django 4.2.6 on 2024-01-06 09:51

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_alter_question_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
