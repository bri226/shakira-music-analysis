import pyodbc
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import CLIENT_ID, CLIENT_SECRET, SERVER, DATABASE


def obtener_datos_artista(nombre_artista: str) -> bool:
    """
    Obtiene los datos de un artista de Spotify y los inserta en una base de datos SQL Server.
    Requiere que existan las siguientes tablas en la base de datos:
    - Artista(Nombre, Genero, Popularidad, Url_Spotify, Seguidores)
    - Album(Nombre_Artista, Nombre_Album, Label, Total_Tracks, Generos, Release_Date)
    - Track(Nombre_Artista, Nombre_Album, Nombre_Track, ID, Duration_ms, Explicit, Artists, Track_Number)
    """

    try:
        # Conexión a la base de datos
        conn_str = (
            r'DRIVER={SQL Server};'
            rf'SERVER={SERVER};'
            rf'DATABASE={DATABASE};'
            r'Trusted_Connection=yes;'
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Configuración de autenticación de Spotify
        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=CLIENT_ID, client_secret=CLIENT_SECRET
            )
        )

        # Buscar artista
        result = sp.search(q=f'artist:{nombre_artista}', type='artist')
        if not result['artists']['items']:
            print(f"No se encontró el artista: {nombre_artista}")
            return False

        artist_info = result['artists']['items'][0]

        # Insertar datos del artista
        artista_data = {
            "Nombre": artist_info.get('name', ''),
            "Genero": ", ".join(artist_info.get('genres', [])),
            "Popularidad": artist_info.get('popularity', None),
            "Url_Spotify": artist_info.get('external_urls', {}).get('spotify', ''),
            "Seguidores": artist_info.get('followers', {}).get('total', None)
        }

        cursor.execute("""
            INSERT INTO Artista (Nombre, Genero, Popularidad, Url_Spotify, Seguidores)
            VALUES (?, ?, ?, ?, ?)
        """, artista_data["Nombre"], artista_data["Genero"], artista_data["Popularidad"],
           artista_data["Url_Spotify"], artista_data["Seguidores"])

        # Obtener álbumes del artista
        albums = sp.artist_albums(artist_info['id'], album_type='album')

        for album in albums['items']:
            album_data = {
                "Nombre_Artista": artist_info.get('name', ''),
                "Nombre_Album": album.get('name', ''),
                "Label": album.get('label', ''),
                "Total_Tracks": album.get('total_tracks', None),
                "Generos": ", ".join(artist_info.get('genres', [])),
                "Release_Date": album.get('release_date', None)
            }

            cursor.execute("""
                INSERT INTO Album (Nombre_Artista, Nombre_Album, Label, Total_Tracks, Generos, Release_Date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, album_data["Nombre_Artista"], album_data["Nombre_Album"], album_data["Label"],
               album_data["Total_Tracks"], album_data["Generos"], album_data["Release_Date"])

            # Obtener pistas del álbum
            tracks = sp.album_tracks(album['id'])

            for track in tracks['items']:
                track_data = {
                    "Nombre_Artista": artist_info.get('name', ''),
                    "Nombre_Album": album.get('name', ''),
                    "Nombre_Track": track.get('name', ''),
                    "ID": track.get('id', None),
                    "Duration_ms": track.get('duration_ms', None),
                    "Explicit": track.get('explicit', False),
                    "Artists": ", ".join([artist['name'] for artist in track.get('artists', [])]),
                    "Track_Number": track.get('track_number', None)
                }

                cursor.execute("""
                    INSERT INTO Track (Nombre_Artista, Nombre_Album, Nombre_Track, ID, Duration_ms, Explicit, Artists, Track_Number)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, track_data["Nombre_Artista"], track_data["Nombre_Album"], track_data["Nombre_Track"],
                   track_data["ID"], track_data["Duration_ms"], track_data["Explicit"],
                   track_data["Artists"], track_data["Track_Number"])

        # Confirmar cambios y cerrar conexión
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Datos del artista '{nombre_artista}' insertados correctamente.")
        return True

    except Exception as e:
        print(f"Error al procesar los datos del artista '{nombre_artista}': {e}")
        return False


if __name__ == "__main__":
    nombre = input("Ingrese el nombre del artista: ") # # nombre = "Shakira"
    
    bool = obtener_datos_artista(nombre)
    if bool:
        print("Los datos se han insertado correctamente en la base de datos.")
    else:
        print("No se pudieron insertar los datos del artista.")
