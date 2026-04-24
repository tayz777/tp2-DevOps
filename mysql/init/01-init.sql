
USE app_db;

CREATE TABLE IF NOT EXISTS utilisateurs (
    id    INT          AUTO_INCREMENT PRIMARY KEY,
    nom   VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role  VARCHAR(50)  NOT NULL
);

INSERT INTO utilisateurs (nom, email, role) VALUES
    ('Zayd El AJLI',    'zayd@example.com',     'admin'),
    ('Glenden AHO',     'glenden@example.com',  'editor'),
    ('Frederic Sturm',  'frederic@example.com', 'author'),
    ('Sacha MOREAU',    'sacha@example.com',    'reader');
