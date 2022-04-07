from esteettomyyssovellus.settings import (
    PUBLIC_AZURE_CONTAINER,
    PUBLIC_AZURE_CONNECTION_STRING,
)

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
