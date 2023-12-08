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
('Phantom Blood', 'Descripción de la Parte 1', 'https://upload.wikimedia.org/wikipedia/en/a/aa/JoJo_Part_1_Phantom_Blood.jpg'),
('Battle Tendency', 'Descripción de la Parte 2', 'https://static.wikia.nocookie.net/jojo/images/9/98/Volumen_11.png/revision/latest?cb=20160214231548&path-prefix=es'),
('Stardust Crusaders', 'Descripción de la Parte 3', 'https://static.wikia.nocookie.net/jojo/images/1/17/Volumen_28.png/revision/latest?cb=20160214230302&path-prefix=es'),
('Diamond is Unbreakable', 'Descripción de la Parte 4', 'https://static.wikia.nocookie.net/jojo/images/9/90/Volumen_46.png/revision/latest?cb=20160216025616&path-prefix=es'),
('Vento Aureo', 'Descripción de la Parte 5', 'https://static.wikia.nocookie.net/jojo/images/1/17/Volumen_63.jpg/revision/latest?cb=20190328214039&path-prefix=es'),
('Stone Ocean', 'Descripción de la Parte 6', 'https://static.wikia.nocookie.net/jojo/images/c/c8/Volumen_80.png/revision/latest?cb=20170808050650&path-prefix=es');


-- Tabla para almacenar los personajes de cada parte
DROP TABLE IF EXISTS personajes;
CREATE TABLE personajes (
    id_personajes INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria_personaje INT(10) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    stand_habilidad VARCHAR(50) NOT NULL,
    referencia_stand VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    nacionalidad VARCHAR(50) NOT NULL,
    imagen_personaje VARCHAR(191) NOT NULL,
    FOREIGN KEY (categoria_personaje) REFERENCES partesJojos(id_parte)
);

-- Insertar datos en la tabla personajes
INSERT INTO personajes (categoria_personaje, nombre, stand_habilidad, referencia_stand, fecha_nacimiento, nacionalidad, imagen_personaje)
VALUES 
(1, 'Jonathan Joestar', 'Hamon - NO Stand', 'Referencia', '1889-02-07', 'Británico', 'https://static.wikia.nocookie.net/jojo/images/7/72/Jonathan_Joestar.png/revision/latest?cb=20160623010314&path-prefix=es'),
(3, 'Jotaro Kujo', 'Star Platinum', 'Tarot Card', '1970-03-20', 'Japonés', 'https://static.wikia.nocookie.net/jojo/images/5/58/Jotarokujo.png/revision/latest?cb=20170302000742&path-prefix=es'),
(2, 'Joseph Joestar', 'Hermit Purple', 'Tarot Card', '1920-09-27', 'Estadounidense', 'https://static.wikia.nocookie.net/jojo/images/5/50/Joseph2manga.jpg/revision/latest?cb=20170131231720&path-prefix=es'),
(4, 'Josuke Higashikata', 'Crazy Diamond', 'Tarot Card', '1983-04-04', 'Japonés', 'https://static.wikia.nocookie.net/jojo/images/f/f8/Josuke_Higashikata.png/revision/latest?cb=20161124070615&path-prefix=es'),
(5, 'Giorno Giovanna', 'Gold Experience', 'Tarot Card', '1985-04-16', 'Italiano', 'https://static.wikia.nocookie.net/jojo/images/f/f6/GiornoP3.png/revision/latest?cb=20170425074254&path-prefix=es'),
(6, 'Jolyne Cujoh', 'Stone Free', 'Tarot Card', '1992-05-10', 'Estadounidense','https://static.wikia.nocookie.net/jojo/images/8/86/Jolyne_Cujoh_en_Stone_Ocean.png/revision/latest?cb=20211126022825&path-prefix=es');
