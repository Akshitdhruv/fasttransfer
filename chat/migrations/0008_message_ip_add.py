# Generated by Django 3.0.7 on 2022-05-09 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_auto_20220508_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='ip_add',
            field=models.CharField(default=0, max_length=1000000),
        ),
    ]
