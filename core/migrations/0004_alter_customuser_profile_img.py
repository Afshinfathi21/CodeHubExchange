# Generated by Django 4.2.6 on 2023-11-16 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_customuser_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_img',
            field=models.ImageField(blank=True, default='/media/src/default_user', upload_to='Users/%Y%m%d'),
        ),
    ]
