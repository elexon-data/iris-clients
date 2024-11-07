from asyncio.log import logger
from datetime import datetime
import asyncio
import os
import sys
import json
import logging
import ast
from dacite import from_dict
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusReceivedMessage
from azure.identity.aio import ClientSecretCredential

from settings import Settings

"""
This async_client example is almost identical to the sync client.
However there are some minor changes, the obvious ones include the
creation of the event loop and prefixing the functions you please
with 'async'. One gotcha that isn't so obvious is that some of the
imports have changed and are now imported with the suffix '.aio'.
"""

def read_settings() -> Settings:
    with open('settings.json', 'r') as config_file:
        settings_dict = json.load(config_file)
        settings = from_dict(Settings, settings_dict)
    return settings

def get_authenticated_sevice_bus_client(settings: Settings):    
    if settings.ClientId and settings.Secret:
        token_credential = ClientSecretCredential(
            settings.TenantId,
            settings.ClientId,
            settings.Secret
        )
        logging.info('Connecting using app registration')
        return ServiceBusClient(settings.FullyQualifiedNamespace, token_credential)
    
    logging.info('No connection string or app registration details found')
    logging.info('Login required to listen to queue')
    return None

async def save_message(msg: ServiceBusReceivedMessage, download_directory):
    """
    You may run async operations in this function too. For example:

    await my_connection.publish(bytes(json.dump(raw_json)))
    """
    raw_json_s = ast.literal_eval(str(msg))
    raw_json = json.loads(raw_json_s)
    dataset = msg.subject or 'unknown'
    file_name = f'{dataset}_{datetime.now().strftime("%y%m%dT%H%M%S_%f")}.json'
    output_folder_path = os.path.join(download_directory, dataset)
    output_file_path = os.path.join(output_folder_path, file_name)
    
    if not os.path.exists(output_folder_path):
        os.mkdir(output_folder_path)

    with open(output_file_path, 'w+') as f:
        logging.info(f"Downloading data to {output_file_path}")
        json.dump(raw_json, f)

def get_download_directory(settings: Settings):
    return settings.RelativeFileDownloadDirectory

async def run():
    """
    You may run async operations in this function. For example:

    my_connection = await get_my_connection()
    """
    settings = read_settings()
    download_directory = get_download_directory(settings)
    client = get_authenticated_sevice_bus_client(settings)

    if not client:
        return

    if not os.path.exists(download_directory):
        os.mkdir(download_directory)

    receiver = client.get_queue_receiver(settings.QueueName)
    logging.info('Connection created with processor')

    with receiver:
        async for msg in receiver:
            try:
                # You may pass in my_connection here
                await save_message(msg, download_directory)
                receiver.complete_message(msg)
                logging.debug(f'Successfully processed message.')
            except Exception as e:
                receiver.abandon_message(msg)
                logging.error(f'Unable to process message. Reason: {e}')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.run_forever()
