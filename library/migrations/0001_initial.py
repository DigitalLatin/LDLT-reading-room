# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-26 20:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xml_id', models.CharField(max_length=100, verbose_name='section id')),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=400)),
                ('title', models.CharField(max_length=1000)),
                ('description', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('source', models.URLField(max_length=400)),
                ('custom_css', models.URLField(verbose_name='custom CSS')),
                ('custom_js', models.URLField(verbose_name='custom JavaScript')),
                ('version', models.CharField(max_length=30)),
                ('replaces', models.CharField(max_length=400)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Edition'),
        ),
    ]
