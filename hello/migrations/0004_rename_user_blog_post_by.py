# Generated by Django 4.0.2 on 2022-12-14 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_blog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='user',
            new_name='post_by',
        ),
    ]
