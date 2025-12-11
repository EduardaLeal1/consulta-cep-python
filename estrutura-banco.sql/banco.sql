 CREATE DATABASE consulta_cep;
 USE consulta_cep;

CREATE TABLE enderecos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cep VARCHAR (9) NOT NULL,
    logradouro VARCHAR(255),
    complemento VARCHAR(255),
    bairro VARCHAR(255),
    localidade VARCHAR(255),
    uf CHAR(2)
    );

    SELECT * FROM enderecos;