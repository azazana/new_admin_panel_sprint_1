CREATE SCHEMA IF NOT EXISTS content;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);



CREATE TABLE IF NOT EXISTS content.genr (
    id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genr_film_work (
    id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY,
    genr_id uuid REFERENCES genr (id) ON DELETE CASCADE,   
    film_work_id uuid REFERENCES film_work (id) ON DELETE CASCADE,
    created timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS "index_genr_film_work"
  ON genr_film_work
  USING btree
  (film_work_id, genr_id);


CREATE TABLE IF NOT EXISTS content.person (
    id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY,
    person_id uuid REFERENCES person (id) ON DELETE CASCADE,
    film_work_id uuid REFERENCES film_work (id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    created timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS "index_person_film_work"
  ON person_film_work
  USING btree
  (film_work_id, person_id);


