DROP TABLE IF EXISTS movie_actors CASCADE;
DROP TABLE IF EXISTS movie_genres CASCADE;
DROP TABLE IF EXISTS movies CASCADE;
DROP TABLE IF EXISTS persons CASCADE; /* For actors, directors */
DROP TABLE IF EXISTS genres CASCADE;

CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE persons (
    person_id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
    -- birth_date DATE -- Not available in CSV, can add later
);

CREATE TABLE movies (
    movie_id INTEGER PRIMARY KEY, -- From CSV ID
    title VARCHAR(255) NOT NULL,
    release_year INTEGER,
    runtime INTEGER, -- in minutes
    rank INTEGER,
    votes INTEGER
);

CREATE TABLE movie_genres (
    movie_id INTEGER REFERENCES movies(movie_id) ON DELETE CASCADE,
    genre_id INTEGER REFERENCES genres(genre_id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, genre_id)
);

CREATE TABLE movie_actors (
    movie_id INTEGER REFERENCES movies(movie_id) ON DELETE CASCADE,
    person_id INTEGER REFERENCES persons(person_id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, person_id)
);

-- Optional: Indexes for faster searching
CREATE INDEX idx_movies_release_year ON movies(release_year);
CREATE INDEX idx_movies_runtime ON movies(runtime);
CREATE INDEX idx_movies_rank ON movies(rank);