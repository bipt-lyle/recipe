# Generated by Django 2.2.25 on 2022-02-09 00:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_filterrecipe2'),
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Uname', models.CharField(max_length=32)),
                ('Email', models.CharField(max_length=32)),
                ('password_hash', models.CharField(max_length=100)),
                ('password_salt', models.CharField(max_length=50)),
                ('status', models.IntegerField(default=1)),
                ('signdate', models.DateTimeField(default=datetime.datetime.now)),
                ('update_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
