# Generated by Django 3.0.4 on 2020-04-10 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vsm', '0002_auto_20200410_2224'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vectorspacemodel',
            old_name='idf_function',
            new_name='idf_func',
        ),
        migrations.RenameField(
            model_name='vectorspacemodel',
            old_name='normalization_function',
            new_name='norm_func',
        ),
        migrations.RenameField(
            model_name='vectorspacemodel',
            old_name='tf_function',
            new_name='tf_func',
        ),
    ]
