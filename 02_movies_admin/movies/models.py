import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.CharField(_('created_at'), max_length=50)
    updated_at = models.CharField(_('updated_at'), max_length=50)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является
        # представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.name

    # Первым аргументом обычно идёт человекочитаемое название поля
    name = models.CharField(_('name'), max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(_('description'), blank=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в
        # классе модели
        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Person(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.full_name

    full_name = models.CharField(_('full_name'), max_length=255)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в
        # классе модели
        db_table = "content\".\"person"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'


class PersonFilmwork(UUIDMixin):
    class TypeRoles(models.TextChoices):
        Director = 'Director'
        Actor = 'Actor'
        Screenwriter = 'Screenwriter'
        Make_up_artist = 'Make_up_artist'

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(_('role'), choices=TypeRoles.choices, null=True)
    created_at = models.CharField(_('created_at'), max_length=50)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в
        # классе модели
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'
        db_table = "content\".\"person_film_work"
        # Почему лучше использовать constraints а не Index?
        constraints = [
            models.UniqueConstraint(
                fields=['film_work_id', 'person_id', 'role'], name='index_person_film_work')
        ]


class Filmwork(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.title

    class TypeFilms(models.TextChoices):
        MOVIE = 'MV', ('movie')
        TV_SHOW = 'TV', ('tv_show')

    # blank=True делает поле необязательным для заполнения.
    title = models.TextField(_('title'), blank=True)
    # Первым аргументом обычно идёт человекочитаемое название поля
    description = models.CharField(_('description'), max_length=255)
    creation_date = models.DateTimeField(_('creation_date'), null=True,)
    rating = models.FloatField(
        _('rating'),
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)], null=True)
    type = models.CharField(_('type'), max_length=2, choices=TypeFilms.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    person = models.ManyToManyField(Person, through='PersonFilmwork')
    certificate = models.CharField(
        _('certificate'), max_length=512, blank=True, null=True,
    )
    # Параметр upload_to указывает, в какой
    # подпапке будут храниться загружемые файлы.
    # Базовая папка указана в файле настроек как MEDIA_ROOT
    file_path = models.FileField(
        _('file'),
        blank=True,
        null=True,
        upload_to='movies/'
    )

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в
        # классе модели
        db_table = "content\".\"film_work"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'
        constraints = [
            models.UniqueConstraint(fields=['creation_date'], name='film_work_creation_date_idx')
        ]


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created_at = models.CharField(_('created_at'), max_length=50)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        constraints = [
            models.UniqueConstraint(fields=['film_work_id', 'genre_id'],
                                    name='index_genre_film_work')
        ]
