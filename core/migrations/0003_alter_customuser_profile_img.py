# Generated by Django 4.2.6 on 2023-11-11 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_customuser_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_img',
            field=models.ImageField(blank=True, upload_to=None),
        ),
    ]
