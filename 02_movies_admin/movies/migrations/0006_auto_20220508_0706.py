# Generated by Django 3.2 on 2022-05-08 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20220501_1450'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filmwork',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='genre',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='created',
            new_name='created_at',
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='certificate',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='certificate'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='creation_date',
            field=models.DateTimeField(null=True, verbose_name='creation_date'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='file_path',
            field=models.FileField(blank=True, null=True, upload_to='movies/', verbose_name='file'),
        ),
    ]
