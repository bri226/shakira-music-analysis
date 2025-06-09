-- Tabla para Artistas
CREATE TABLE Artista (
    Nombre NVARCHAR(255) NOT NULL,
    Genero NVARCHAR(255),
    Popularidad INT,
    Url_Spotify NVARCHAR(255),
    Seguidores INT
);

-- Tabla para �lbumes
CREATE TABLE Album (
    Nombre_Artista NVARCHAR(255) NOT NULL,
    Nombre_Album NVARCHAR(255) NOT NULL,
    Label NVARCHAR(255),
    Total_Tracks INT,
    Generos NVARCHAR(MAX),
    Release_Date DATE
);

-- Tabla para Pistas (Tracks)
CREATE TABLE Track (
    Nombre_Artista NVARCHAR(255) NOT NULL,
    Nombre_Album NVARCHAR(255) NOT NULL,
	Nombre_Track NVARCHAR(255) NOT NULL,
    --Disc_Number INT,
    Duration_ms INT,
    Explicit BIT,
    Artists NVARCHAR(MAX),
    Track_Number INT
    --Popularidad NVARCHAR(10)
);

CREATE TABLE Track_Features (
    Nombre_Artista NVARCHAR(255),
    Nombre_Album NVARCHAR(255),
    Nombre_Track NVARCHAR(255),
    ID NVARCHAR(50),
    Duration_ms INT,
    Explicit BIT,
    Artists NVARCHAR(MAX),
    Track_Number INT,
    acousticness FLOAT,
    danceability FLOAT,
    energy FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    loudness FLOAT,
    speechiness FLOAT,
    tempo FLOAT,
    valence FLOAT,
    analysis_url NVARCHAR(255),
    [key] INT,
    mode INT,
    time_signature INT
);

CREATE TABLE Track_Features_2 (
    Nombre_Artista NVARCHAR(255),
    Nombre_Album NVARCHAR(255),
    Nombre_Track NVARCHAR(255),
    ID NVARCHAR(50),
    Duration_ms INT,
    Explicit BIT,
    Artists NVARCHAR(MAX),
    Track_Number INT,
    acousticness FLOAT,
    danceability FLOAT,
    energy FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    loudness FLOAT,
    speechiness FLOAT,
    tempo FLOAT,
    valence FLOAT,
    analysis_url NVARCHAR(255),
    [key] INT,
    mode INT,
    time_signature INT,
    popularity INT
);

select * from Artista where Nombre = 'Tini'
select * from Album where Nombre_Artista = 'Shakira'
select * from Track where Nombre_Artista = 'Tini'

truncate table Artista;
truncate table Album;
truncate table Track;

drop table Artista;
drop table Album;
drop table Track;

select * into Track_Limpio from Track

-- Calcular por album
SELECT 
    Nombre_Album,
    AVG(acousticness) AS avg_acousticness,
    STDEV(acousticness) AS std_acousticness,
    AVG(danceability) AS avg_danceability,
    STDEV(danceability) AS std_danceability,
    AVG(energy) AS avg_energy,
    STDEV(energy) AS std_energy,
    AVG(instrumentalness) AS avg_instrumentalness,
    STDEV(instrumentalness) AS std_instrumentalness,
    AVG(liveness) AS avg_liveness,
    STDEV(liveness) AS std_liveness,
    AVG(loudness) AS avg_loudness,
    STDEV(loudness) AS std_loudness,
    AVG(speechiness) AS avg_speechiness,
    STDEV(speechiness) AS std_speechiness,
    AVG(tempo) AS avg_tempo,
    STDEV(tempo) AS std_tempo,
    AVG(valence) AS avg_valence,
    STDEV(valence) AS std_valence,
    AVG(mode) AS avg_mode,
    STDEV(mode) AS std_mode,
    AVG(time_signature) AS avg_time_signature,
    STDEV(time_signature) AS std_time_signature
FROM 
    Track_Features
GROUP BY 
    Nombre_Album
ORDER BY 
    Nombre_Album;
