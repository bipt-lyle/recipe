# Generated by Django 2.2.25 on 2022-01-18 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_filterrecipe'),
    ]

    operations = [
        migrations.CreateModel(
            name='flavor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flavor', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'flavor',
            },
        ),
    ]
