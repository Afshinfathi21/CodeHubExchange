# Generated by Django 4.2.6 on 2023-12-07 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_discution_alter_customuser_profile_img_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='question',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='Discution',
        ),
        migrations.RemoveField(
            model_name='question',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='question',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='vote',
            name='question',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
