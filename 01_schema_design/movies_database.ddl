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
    film_work_id uuid REFERENCES film_work ON DELETE CASCADE,
    genr_id uuid REFERENCES genr ON DELETE CASCADE,   
    created timestamp with time zone,
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    person_film_work_id uuid REFERENCES person_film_work ON DELETE CASCADE,
    film_work_id uuid REFERENCES film_work ON DELETE CASCADE,
    role TEXT NOT NULL,
    created timestamp with time zone,
);


