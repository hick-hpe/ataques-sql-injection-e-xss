
CREATE DATABASE IF NOT EXISTS app_posts_vulneravel;
CREATE DATABASE IF NOT EXISTS app_posts_seguro;

GRANT ALL PRIVILEGES ON app_posts_vulneravel.*
TO 'app_user'@'%';

GRANT ALL PRIVILEGES ON app_posts_seguro.*
TO 'app_user'@'%';


-- BANCO VULNERÁVEL
USE app_posts_vulneravel;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    conteudo TEXT NOT NULL,
    usuario_id INT NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
);

INSERT IGNORE INTO usuarios (usuario, senha)
VALUES ('admin', 'admin123');


-- BANCO SEGURO
USE app_posts_seguro;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    conteudo TEXT NOT NULL,
    usuario_id INT NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
);

INSERT IGNORE INTO usuarios (usuario, senha)
VALUES ('admin', 'admin123');
