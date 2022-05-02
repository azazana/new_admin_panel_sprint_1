from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description')


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 3
    max_num = 3


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    extra = 3
    max_num = 3


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,)
    list_display = ('title', 'type', 'creation_date', 'rating',)
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')
    #model = Filmwork.questions.through


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name', )
