# Generated by Django 4.0.2 on 2022-12-13 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilepik',
            name='postby_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
