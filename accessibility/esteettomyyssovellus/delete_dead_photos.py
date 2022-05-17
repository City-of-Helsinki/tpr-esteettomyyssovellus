# THIS SCRIPT SHOULD BE RUN WITH A CERTAIN TIME INTERVAL. IT REMOVES DEAD PHOTOS FROM AZURE.
import os
import environ

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "esteettomyyssovellus.settings")

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    FORCE_SCRIPT_NAME=(str, ""),
    FULL_WEB_ADDRESS=(str, "http://localhost"),
)

env.read_env()

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DB_USER = env("DB_USER")
DB_PASSWORD = env("DB_PASSWORD")
DB_HOST = env("DB_HOST")
DB_PORT = env("DB_PORT")
DB = env("DB")
API_TOKEN = env("API_TOKEN")
SEARCH_PATH = env("SEARCH_PATH")
AZURE_URL = env("AZURE_URL")
PUBLIC_AZURE_CONTAINER = env("PUBLIC_AZURE_CONTAINER")
PUBLIC_AZURE_CONNECTION_STRING = env("PUBLIC_AZURE_CONNECTION_STRING")

import psycopg2
import psycopg2.extras
from azure.storage.blob import BlobClient


def create_blob_client(servicepoint_id=None, file_name=None):

    blob_name = ""
    if file_name != None:
        blob_name = file_name
    if servicepoint_id != None:
        blob_name = servicepoint_id + "/" + file_name

    return BlobClient.from_connection_string(
        conn_str=PUBLIC_AZURE_CONNECTION_STRING,
        container_name=PUBLIC_AZURE_CONTAINER,
        blob_name=blob_name,
    )


def delete_from_azure(servicepoint_id=None, file_name=None):
    try:
        blob_service_client = create_blob_client(servicepoint_id, file_name)
        blob_service_client.delete_blob()
        return True
    except Exception as e:
        return False


def arp_dead_photo_remove(photo_url):

    try:
        ps_connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB,
            options="-c search_path={}".format(SEARCH_PATH),
        )

        cursor = ps_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Call the psql function that removes the photo.
        cursor.execute("SELECT arp_dead_photo_remove(%s)", [photo_url])

        # Get the returned values
        result = cursor.fetchall()
        ps_connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while using database function:", error)
        return False
    finally:
        # closing database connection.
        if ps_connection:
            cursor.close()
            ps_connection.close()
            print("PostgreSQL connection is closed")
        return True


def main():
    print("***Start script***")
    try:
        print("Connecting to database...")
        ps_connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB,
            options="-c search_path={}".format(SEARCH_PATH),
        )

        cursor = ps_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Call the psql function that chops the address
        cursor.execute("SELECT photo_url from ar_backend_dead_photo")

        # Get the returned values
        result = cursor.fetchall()
        print(len(result), "dead picture(s) found.")

    except (Exception, psycopg2.Error) as error:
        print("Error while selecting values.", error)
        result = []
    finally:
        cursor.close()
        ps_connection.close()
        print("PostgreSQL connection is closed")

    photo_urls = [d["photo_url"] for d in result]
    if len(photo_urls) == 0:
        print("No photo_urls to delete.")

    count = 0

    for url in photo_urls:
        if not url is None and AZURE_URL in url:
            servicepoint_id = url.split("/")[-2]
            file_name = url.split("/")[-1]
            deleted = delete_from_azure(servicepoint_id, file_name)
            if deleted:
                removed_from_db = arp_dead_photo_remove(url)
                if removed_from_db:
                    print("Dead picture removed from database. URL:", url)
                    count += 1
                else:
                    print(
                        "Dead picture was not able to be removed from database. URL:",
                        url,
                    )
        elif not url is None:
            removed_from_db = arp_dead_photo_remove(url)
            if removed_from_db:
                print("Dead picture removed from database. URL:", url)
                count += 1
            else:
                print(
                    "Dead picture was not able to be removed from database. URL:", url
                )
        else:
            print("Dead picture was not able to be removed from database. URL:", url)

    print("Script completed. Pictures removed:", count)


if __name__ == "__main__":
    main()
