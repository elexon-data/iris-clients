from datetime import datetime
import os
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


def get_authenticated_service_bus_client(settings: Settings):
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
    browser_credential = InteractiveBrowserCredential(tenant_id=settings.TenantId)
    return ServiceBusClient(settings.FullyQualifiedNamespace, browser_credential)


def save_message(msg: ServiceBusReceivedMessage, download_directory):
    raw_json_s = ast.literal_eval(str(msg))
    raw_json = json.loads(raw_json_s)
    dataset = msg.subject or 'unknown'

    file_name = msg.message_id
    if not file_name:
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


def run():
    settings = read_settings()
    download_directory = get_download_directory(settings)
    client = get_authenticated_service_bus_client(settings)
    if not os.path.exists(download_directory):
        os.mkdir(download_directory)

    receiver = client.get_queue_receiver(settings.QueueName)
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
