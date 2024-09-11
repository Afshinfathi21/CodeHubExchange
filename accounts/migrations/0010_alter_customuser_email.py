# Generated by Django 4.2.6 on 2024-05-24 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_customuser_github_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(error_messages={'blank': 'این فیلد نمی\u200cتواند خالی باشد.', 'invalid': 'لطفاً یک آدرس ایمیل معتبر وارد کنید.', 'unique': 'این ایمیل قبلاً ثبت شده است.'}, max_length=254, unique=True),
        ),
    ]
