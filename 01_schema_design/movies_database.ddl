CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genr (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genr_film_work (
    id uuid PRIMARY KEY,
    created timestamp with time zone,
);

CREATE TABLE IF NOT EXISTS genr_film_work_genr (
    genr_id uuid REFERENCES genr ON DELETE CASCADE,
    genr_film_work_id uuid REFERENCES genr_film_work ON DELETE CASCADE,
    PRIMARY KEY (genr_id, genr_film_work_id)
);

CREATE TABLE IF NOT EXISTS genr_film_work_film_work (
    genr_id uuid REFERENCES genr ON DELETE CASCADE,
    film_work_id uuid REFERENCES film_work ON DELETE CASCADE,
    PRIMARY KEY (genr_id, film_work_id)
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    role TEXT NOT NULL,
    created timestamp with time zone,
);

CREATE TABLE IF NOT EXISTS content.person_film_work_person (
    person_id uuid REFERENCES person ON DELETE CASCADE,
    person_film_work_id uuid REFERENCES person_film_work ON DELETE CASCADE,
    PRIMARY KEY (person_id, person_film_work_id)
);


CREATE TABLE IF NOT EXISTS content.person_film_work_film_work (
    film_work_id uuid REFERENCES film_work ON DELETE CASCADE,
    person_film_work_id uuid REFERENCES person_film_work ON DELETE CASCADE,
    PRIMARY KEY (film_work_id, person_film_work_id)
);



