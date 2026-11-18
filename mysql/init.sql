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

-- Usuário inicial para testes
INSERT IGNORE INTO usuarios (usuario, senha)
VALUES ('admin', 'admin123');

-- Usuário inicial para testes
INSERT IGNORE INTO usuarios (usuario, senha)
VALUES ('test1', 'test123');

-- Usuário inicial para testes
INSERT IGNORE INTO usuarios (usuario, senha)
VALUES ('test2', 'test123');
