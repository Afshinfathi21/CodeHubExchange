# Generated by Django 4.2.6 on 2024-05-05 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0007_remove_tag_department_tag_department'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Topic'},
        ),
        migrations.AddField(
            model_name='tag',
            name='approve',
            field=models.BooleanField(default=False),
        ),
    ]
