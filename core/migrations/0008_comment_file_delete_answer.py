# Generated by Django 4.2.6 on 2023-11-30 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_question_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=None),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
    ]
