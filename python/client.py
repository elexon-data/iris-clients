from asyncio.log import logger
from datetime import datetime
import os
import sys
import json
import logging
import ast
from dacite import from_dict
from azure.servicebus import ServiceBusClient, ServiceBusReceivedMessage
from azure.identity import ClientSecretCredential, InteractiveBrowserCredential

from settings import Settings

def read_settings() -> Settings:
    with open('settings.json', 'r') as config_file:
        settings_dict = json.load(config_file)
        settings = from_dict(Settings, settings_dict)
    return settings

def get_authenticated_sevice_bus_client(settings: Settings):    
    if settings.AppRegistration.ClientId and settings.AppRegistration.Secret:
        token_credential = ClientSecretCredential(
            settings.TenantId,
            settings.AppRegistration.ClientId,
            settings.AppRegistration.Secret
        )
        logging.info('Connecting using app registration')
        return ServiceBusClient(settings.FullyQualifiedNamespace, token_credential)
    
    logging.info('No connection string or app registration details found')
    logging.info('Login required to listen to queue')
    browser_credential = InteractiveBrowserCredential(tenant_id=settings.TenantId)
    return ServiceBusClient(settings.FullyQualifiedNamespace, browser_credential)

def save_message(msg: ServiceBusReceivedMessage, download_directory):
    raw_json_s = ast.literal_eval(str(msg))
    raw_json = json.loads(raw_json_s)
    dataset = raw_json[0]['dataset'] or 'unknown'
    file_name = f'{dataset}_{datetime.now().strftime("%y%m%dT%H%M%S_%f")}.json'
    output_folder_path = os.path.join(download_directory, dataset)
    output_file_path = os.path.join(output_folder_path, file_name)
    
    if not os.path.exists(output_folder_path):
        os.mkdir(output_folder_path)

    with open(output_file_path, 'w+') as f:
        logging.info(f"Downloading data to {output_file_path}")
        json.dump(raw_json, f)

def get_download_directory(settings: Settings):
    if settings.RelativeFileDownloadDirectory and (not settings.RelativeFileDownloadDirectory.isspace()):
        return settings.RelativeFileDownloadDirectory
    else:
        sys.exit('Invalid configuration value: RelativeFileDownloadDirectory is required')

def run():
    settings = read_settings()
    download_directory = get_download_directory(settings)
    client = get_authenticated_sevice_bus_client(settings)
    if not os.path.exists(download_directory):
        os.mkdir(download_directory)

    receiver = client.get_queue_receiver(settings.ServiceBusQueue)
    logging.info('Connection created with processor')

    with receiver:
        for msg in receiver:
            try:
                save_message(msg, download_directory)
                receiver.complete_message(msg)
                logging.debug(f'Successfully processed message.')
            except Exception as e:
                receiver.abandon_message(msg)
                logging.error(f'Unable to process message. Reason: {e}')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
    
