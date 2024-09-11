# Generated by Django 4.2.6 on 2023-11-16 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_customuser_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_img',
            field=models.ImageField(blank=True, default='src/default_user.png', upload_to='Users/%Y%m%d'),
        ),
        migrations.RemoveField(
            model_name='question',
            name='tag',
        ),
        migrations.AddField(
            model_name='question',
            name='tag',
            field=models.ManyToManyField(to='core.tag'),
        ),
    ]
