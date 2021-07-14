import json
import requests
import os
from PIL import Image
from io import BytesIO
from azure.storage.blob import ContainerClient
from datetime import datetime, timedelta
from config.config import WHATSAPP_URL

class WhatsappUtility():

    def get_Name(self, record):
        if record.get('metadata')['name'] is not None:
            fullname = record.get('metadata')['name']
            return fullname
        else:
            return None

    def download_media(self, media_id, sender_id, msg_type, metadata):
        url = WHATSAPP_URL+"/api/v1/messages"

        headers = {
            'Content-Type': 'application/json',
        }

        r = requests.request("GET", url, headers=headers, data='')
        
        cwd = os.getcwd()
        file_name = str(sender_id)
        if msg_type == 'image':
            if metadata == 'image/jpeg':
                file_name += '_' + str(media_id) + '.jpg'
            elif metadata == 'image/png':
                file_name += '_' + str(media_id) + '.png'
            file_loc = cwd + '/' + file_name
            print('image downloaded')
        
        elif msg_type == 'video':
            if metadata == 'video/mp4':
                file_name += '_' + str(media_id) + '.mp4'
            file_loc = cwd + '/' + file_name
            print('gif/video downloaded')
        
        elif msg_type == 'audio':
            if metadata == 'audio/mpeg':
                file_name += '_' + str(media_id) + '.mp3'
            file_loc = cwd + '/' + file_name
            print('audio downloaded')
        
        elif msg_type == 'voice':
            if metadata == 'audio/ogg; codecs=opus':
                file_name += '_' + str(media_id) + '.mp3'
            file_loc = cwd + '/' + file_name
            print('audio downloaded')
        
        elif msg_type == 'document':
            extension = metadata.split('.')[-1]
            file_name += '_' + str(media_id) + '.' + extension
            file_loc = cwd + '/' + file_name
            print('document downloaded')
        
        b = r.content
        f = open(file_name, 'wb')
        f.write(b)
        f.close()
        return file_loc, file_name

    def upload_to_cdn(self, bot_name, file_loc, file_name, container_root_url, connection_string, container_name):
        container_client = ContainerClient.from_connection_string(connection_string, container_name)
        file_name = bot_name + '/' + file_name
        blob_client =container_client.get_blob_client(file_name)
        with open(file_loc, 'rb') as data:
            blob_client.upload_blob(data)
            print('Upload Done: ' + file_name)
            os.remove(file_loc)
            image_url = container_root_url + '/' + container_name + '/' + file_name
            return image_url
