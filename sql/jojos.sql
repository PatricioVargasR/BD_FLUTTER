-- Script para almacenar información sobre mascotas --

-- Tabla para almacenar las partes de la serie de Jojos

DROP TABLE IF EXISTS partesJojos;
CREATE TABLE partesJojos (
    id_parte INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_parte VARCHAR(191) NOT NULL,
    descripcion_parte LONGTEXT NOT NULL,
    imagen_parte VARCHAR(191) NOT NULL
);


-- Insertar datos en la tabla partesJojos
INSERT INTO partesJojos (nombre_parte, descripcion_parte, imagen_parte)
VALUES
('Parte 1', 'Descripción de la Parte 1', 'imagen_parte1.jpg'),
('Parte 2', 'Descripción de la Parte 2', 'imagen_parte2.jpg'),
('Parte 3', 'Descripción de la Parte 3', 'imagen_parte3.jpg'),
('Parte 4', 'Descripción de la Parte 4', 'imagen_parte4.jpg'),
('Parte 5', 'Descripción de la Parte 5', 'imagen_parte5.jpg');


-- Tabla para almacenar los personajes de cada parte
DROP TABLE IF EXISTS personajes;
CREATE TABLE personajes (
    id_personajes INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria_personaje INT(10) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    stand_habilidad VARCHAR(50) NOT NULL,
    referencia_stand VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    fecha_muerte DATE,
    genero VARCHAR(15) NOT NULL,
    altura VARCHAR(15) NOT NULL,
    peso VARCHAR(15) NOT NULL,
    nacionalidad VARCHAR(50) NOT NULL,
    descripcion LONGTEXT NOT NULL,
    imagen_personaje VARCHAR(191) NOT NULL,
    FOREIGN KEY (categoria_personaje) REFERENCES partesJojos(id_parte)
);

-- Insertar datos en la tabla personajes
INSERT INTO personajes (categoria_personaje, nombre, stand_habilidad, referencia_stand, fecha_nacimiento, fecha_muerte, genero, altura, peso, nacionalidad, descripcion, imagen_personaje)
VALUES 
(1, 'Jotaro Kujo', 'Star Platinum', 'Tarot Card', '1970-03-20', NULL, 'Masculino', '195 cm', '82 kg', 'Japonés', 'Descripción de Jotaro Kujo', 'jotaro.jpg'),
(2, 'Joseph Joestar', 'Hermit Purple', 'Tarot Card', '1920-09-27', '2019-09-27', 'Masculino', '183 cm', '75 kg', 'Estadounidense', 'Descripción de Joseph Joestar', 'joseph.jpg'),
(3, 'Josuke Higashikata', 'Crazy Diamond', 'Tarot Card', '1983-04-04', NULL, 'Masculino', '178 cm', '72 kg', 'Japonés', 'Descripción de Josuke Higashikata', 'josuke.jpg'),
(4, 'Giorno Giovanna', 'Gold Experience', 'Tarot Card', '1985-04-16', NULL, 'Masculino', '175 cm', '68 kg', 'Italiano', 'Descripción de Giorno Giovanna', 'giorno.jpg'),
(5, 'Jolyne Cujoh', 'Stone Free', 'Tarot Card', '1992-05-10', NULL, 'Femenino', '175 cm', '55 kg', 'Estadounidense', 'Descripción de Jolyne Cujoh', 'jolyne.jpg');
