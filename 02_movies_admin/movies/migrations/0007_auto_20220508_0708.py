# Generated by Django 3.2 on 2022-05-08 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20220508_0706'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filmwork',
            old_name='modified',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='genre',
            old_name='modified',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='modified',
            new_name='updated_at',
        ),
    ]
