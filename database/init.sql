CREATE DATABASE IF NOT EXISTS database;

\c database;

CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    ano INT NOT NULL,
    diretor VARCHAR(255) NOT NULL
);

INSERT INTO movies (titulo, ano, diretor) VALUES
('The Shawshank Redemption', 1994, 'Frank Darabont'),
('The Godfather', 1972, 'Francis Ford Coppola'),
('The Dark Knight', 2008, 'Christopher Nolan'),
('Pulp Fiction', 1994, 'Quentin Tarantino'),
('The Lord of the Rings: The Return of the King', 2003, 'Peter Jackson'),
('Forrest Gump', 1994, 'Robert Zemeckis'),
('Inception', 2010, 'Christopher Nolan'),
('The Matrix', 1999, 'The Wachowskis'),
('Goodfellas', 1990, 'Martin Scorsese'),
('The Empire Strikes Back', 1980, 'Irvin Kershner');
