# Generated by Django 3.2.2 on 2021-12-01 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0005_auto_20211201_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title_tag',
            field=models.CharField(default='My blog!', max_length=255),
        ),
    ]
