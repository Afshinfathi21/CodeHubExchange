# Generated by Django 4.2.6 on 2024-04-09 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_github_link_customuser_linkdin_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='uid',
            field=models.CharField(max_length=11, null=True),
        ),
    ]
