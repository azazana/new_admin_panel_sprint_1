# Generated by Django 3.2 on 2022-05-01 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_alter_filmwork_title'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE "content"."genre_film_work"
                ADD CONSTRAINT "genre_film_work_film_work_id_genre_id_uniq"
                UNIQUE ("film_work_id", "genre_id");
            """,
            reverse_sql='ALTER TABLE "content"."genre_film_work" DROP CONSTRAINT genre_film_work_film_work_id_genre_id_uniq',
        )]
