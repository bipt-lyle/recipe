# Generated by Django 2.2.25 on 2022-02-13 21:15

from django.db import migrations, models
import django.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_delete_coments'),
    ]

    operations = [
        migrations.CreateModel(
            name='coments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('com', models.TextField(verbose_name='留言')),
                ('tim', models.DateTimeField(auto_now_add=True)),
                ('To', models.ForeignKey(on_delete=django.db.models.fields.NOT_PROVIDED, related_name='comen', to='myapp.therecipes')),
            ],
        ),
    ]
