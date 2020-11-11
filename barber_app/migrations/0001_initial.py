# Generated by Django 2.0.13 on 2020-11-11 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=250)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('body', models.TextField(blank=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
