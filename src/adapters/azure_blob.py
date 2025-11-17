import os
import json
import logging
import pickle

from azure.storage.blob import BlobClient, BlobServiceClient

from dotenv import load_dotenv
load_dotenv()


class AzureBlob():
    '''
    This class has a set of functions defined for uploading files, accessing file, initiazing azure blob storage object, downloading and getting the size of a file on blob containers
    '''

    def __init__(self) -> None:
        self.logger = logging.getLogger('ct-logger-azure-blob')
        self.BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
        # super().__init__()

    def initialize_blob_client(self, file_name, blob_container_name):
        """
        This method establishes connection to the blob storage and returns the container object.
        input:
            file_name -> It contains the name of the file in string format. Ex: "oil-and-gas-handbook.pdf"
            blob_container_name -> It contains the name of the Azure blob container in string format. Ex: "ctminerv3"
        output:
            blob_client -> The blob_client object for performing upload, download, read operations on blob container if the connection is successfully established or else return False
        """
        blob_service_client = BlobServiceClient.from_connection_string(
            self.BLOB_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(
            container=blob_container_name, blob=file_name)
        return blob_client

    def upload_blob(self, filepath, file_name, blob_container_name):
        """
        This method uploads the file on azure blob container
        input:
            filepath -> It contains the path to the file in string format.
            folder_name -> It contains the name of the folder on blob container in string format.
            blob_container_name -> It contains the name of the azure blob container
        output:
            True -> if the file is succesfully uploaded on azure blob container
            False ->  if the file is not uploaded on azure blob container
        
        """
        self.logger.info(f"[BLOB] Uploading {filepath}")
        blob_client = self.initialize_blob_client(
            file_name, blob_container_name)
        with open(filepath, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

    def list_all_containers(self):
        blob_service_client = BlobServiceClient.from_connection_string(
            self.BLOB_CONNECTION_STRING)
        containers = [container['name']
                      for container in blob_service_client.list_containers()]
        return containers

    def list_all_blobs_in_container(self, blob_container_name):
        """
        This method reads all the azure blob containers from the azure storage account.
        input:
            folder_name -> It contains the name of the folder on blob container in string format.
            blob_container_name -> It contains the name of the azure blob container
            
        output:
            listf -> list of all container in list of tuples format.
        """
        try:
            blob_service_client = BlobServiceClient.from_connection_string(
                self.BLOB_CONNECTION_STRING)
            container_client = blob_service_client.get_container_client(
                blob_container_name)
            blobs_list = container_client.list_blobs()
            listf = [i['name'] for i in blobs_list]
            blob_service_client.close()
            return listf
        except Exception as e:
            print(f"Exception in list_all_blobs_in_container() : {e}")

    def get_files_blob(self, blob_name, blob_container_name):
        """
        This method reads all the files from azure blob container.
        input:
            folder_name -> It contains the name of the folder on blob container in string format.
            blob_container_name -> It contains the name of the azure blob container
            blob_connection_string -> It contains the connection string of the storage account to establish connection to the blob container.
        output:
            data -> list of all file details in list of dict format.
        """
        blob_client = BlobClient.from_connection_string(
            self.BLOB_CONNECTION_STRING, blob_container_name, blob_name)
        downloader = blob_client.download_blob(0)
        data = downloader.readall()
        blob_client.close()
        return data
    
    def download_blob(self, blob_name, blob_container_name):
        blob_client = BlobClient.from_connection_string(
            self.BLOB_CONNECTION_STRING, blob_container_name, blob_name)
        if blob_client.exists():
            with open(blob_name, "wb") as fp:
                blob_data = blob_client.download_blob()
                blob_data.readinto(fp)
            return "Blob Downloaded!"
        else:
            return "Blob Not Found!"

    def is_file_present_inside_container(self, file_name, container_name):
        """This function checks for the presence of a file in the respective container.

        Args:
            file_name (str): file to be checked
            container_name (str): container in which file existence needs to be checked

        Returns:
            bool: True, if present. Otherwise False
        """
        try:
            flag = False
            conatiner_files_list = self.list_all_blobs_in_container(
                container_name)
            if file_name in conatiner_files_list:
                flag = True
            return flag
        except Exception as e:
            print("Exception in is_file_present_inside_container() : {e}")

    def delete_blob(self, file_name, blob_container_name):
        blob_client = self.initialize_blob_client(
            file_name, blob_container_name)
        blob_client.delete_blob()
        return "deleted successfully"


if __name__ == "__main__":
    azure_blob = AzureBlob()
    print(azure_blob.list_all_blobs_in_container("spnipocs"))
