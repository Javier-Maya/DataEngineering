CREATE TABLE pokemon (
    id INT PRIMARY KEY,
    nombre VARCHAR(255),
    altura DECIMAL(5,2),
    peso DECIMAL(5,2),
    tipo VARCHAR(255),
    movimientos VARCHAR(MAX),
    debilidades VARCHAR(MAX)
);