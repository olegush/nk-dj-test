# Generated by Django 2.2.6 on 2019-10-02 06:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
