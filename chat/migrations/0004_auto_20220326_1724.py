# Generated by Django 3.0.7 on 2022-03-26 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20220326_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='value',
            field=models.FileField(upload_to='media/'),
        ),
    ]
