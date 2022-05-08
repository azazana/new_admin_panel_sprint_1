# Generated by Django 3.2 on 2022-05-01 08:21

import uuid

import django
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4,
                                        editable=False, primary_key=True,
                                        serialize=False,
                                        ),
                 ),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(
                    blank=True, verbose_name='description')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'db_table': 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name='Filmwork',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4,
                                        editable=False, primary_key=True, serialize=False
                                        )),
                ('description', models.CharField(
                    max_length=255, verbose_name='description',
                )),
                ('title', models.TextField(blank=True, verbose_name='title'
                                           )),
                ('file_path', models.TextField(blank=True,
                                               null=True,
                                               # upload_to='movies/',
                                               verbose_name='file'
                                               )),
                ('creation_date', models.DateTimeField(null=True)),
                ('certificate', models.TextField(blank=True, max_length=512,
                                                 verbose_name='certificate',
                                                 null=True,
                                                 )),
                ('rating', models.FloatField(blank=True,
                                             validators=[django.core.validators.MinValueValidator(0),
                                                         django.core.validators.MaxValueValidator(
                                                             100)
                                                         ],
                                             verbose_name='rating'
                                             )
                 ),
                ('type',
                 models.CharField(choices=[('MV', 'movie'),
                                           ('TV', 'tv_show')], max_length=2, verbose_name='type')),
            ],
            options={
                'verbose_name': 'Кинопроизведение',
                'verbose_name_plural': 'Кинопроизведения',
                'db_table': 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4,
                                        editable=False, primary_key=True, serialize=False,
                                        )
                 ),
                ('full_name', models.CharField(
                    max_length=255, verbose_name='full_name',
                ),
                 ),
            ],
            options={
                'verbose_name': 'Актер',
                'verbose_name_plural': 'Актеры',
                'db_table': 'content"."person',
            },
        ),
        migrations.CreateModel(
            name='PersonFilmwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4,
                                        editable=False, primary_key=True,
                                        serialize=False,
                                        ),
                 ),
                ('role', models.TextField(null=True, verbose_name='role')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('film_work', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='movies.filmwork',
                ),
                 ),
                ('person', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='movies.person',
                )
                 ),
            ],
            options={
                'db_table': 'content"."person_film_work',
            },
        ),
        migrations.CreateModel(
            name='GenreFilmwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4,
                                        editable=False,
                                        primary_key=True,
                                        serialize=False,
                                        ),
                 ),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('film_work', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='movies.filmwork',
                ),
                 ),
                ('genre', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='movies.genre',
                )),
            ],
            options={
                'db_table': 'content"."genre_film_work',
            },
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(
                through='movies.GenreFilmwork', to='movies.Genre',
            ),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='person',
            field=models.ManyToManyField(
                through='movies.PersonFilmwork', to='movies.Person',
            ),
        ),
    ]
