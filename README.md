![Insights Solution logo](./images/insights-solution.png)

# IRIS clients

The Insights Real-time Information Service (IRIS)  is a near real-time, free, publicly available push service for accessing [Insights Solution](https://bmrs.elexon.co.uk/iris) data.

IRIS is based on the [Advanced Message Queuing Protocol (AMQP)](https://en.wikipedia.org/wiki/Advanced_Message_Queuing_Protocol) open-source standard and you will need a message client to access the data.

This repo contains a collection of example clients along with notes on how to write you own client.


Currently we have clients written in **Python**, **Node.js** and **C#/.NET**.



## Before you begin

All clients will require you to enter your client credentials:
- queue name
- client ID
- client secret

You can request credentials on the [Insights Solution](https://bmrs.elexon.co.uk/iris).

⚠️**Client secrets expire after 2 years** - you need to return to the [Insights Solution](https://bmrs.elexon.co.uk/iris) to generate new secrets.

## Quick-start instructions

To get started with an example client, clone this repo then follow the steps below

<details>
    <summary ><h3>Python</h3></summary>

1. Ensure you have installed [Python](https://www.python.org/downloads/) (version 3.9 or above)
2. Run `cd python` to navigate to the `python` directory
3. Run the following to activate a virtual environment and install the dependencies

```bash
python -m venv .venv
./.venv/Scripts/activate
pip install -r requirements.txt
```
4. Copy the `settings.template.json` file and rename it to `settings.json`
5. Enter your client credentials into the `settings.json` file

```json
{
  "ClientId": "",
  "QueueName": "",
  "ServiceBusNamespace": "elexon-iris",
  "Secret": "",
  "RelativeFileDownloadDirectory": "./data"
}
```
6. Run `python client.py`

N.B. If you leave `ClientId` and `Secret` blank when running the client, it will open a browser window with a login page.
This may be useful during initial setup and testing but is not recommended for production use. 

</details>

<details>
    <summary><h3>Node.js</h3></summary>

1. Ensure you have installed [Node.js](https://nodejs.org/en/) (version 16.0.0 or above)
2. Run `cd nodeJs` to navigate to the `nodeJs` directory
3. Run `npm i` to install the dependencies
4. Copy the `.env.template` file and rename it to `.env`
5. Enter your client credentials into the `.env` file
```
SERVICE_BUS_NAMESPACE=elexon-iris
SERVICE_BUS_QUEUE=
RELATIVE_FILE_DOWNLOAD_DIRECTORY=./data
APP_REGISTRATION_CLIENT_ID=
APP_REGISTRATION_SECRET=
```
6. Run `npm run client`

N.B. If you leave `APP_REGISTRATION_CLIENT_ID` and `APP_REGISTRATION_SECRET` blank when running the client, it will open a browser window with a login page.
This may be useful during initial setup and testing but is not recommended for production use.

</details>

<details>
    <summary ><h3>C#/.NET</h3></summary>

1. Ensure you have installed the [.NET SDK](https://dotnet.microsoft.com/en-us/download/visual-studio-sdks?cid=getdotnetsdk) (version 6 or above)
2. Run `cd dotnet/IrisClient` to navigate to the `dotnet/IrisClient` directory
3. Copy the `appsettings.template.json` file and rename it to `appsettings.json`
4. Enter your client credentials into the `appsettings.json` file

```json
{
  "ClientId": "",
  "QueueName": "",
  "ServiceBusNamespace": "elexon-iris",
  "Secret": "",
  "RelativeFileDownloadDirectory": "./data"
}
```
5. Run `dotnet build` to build the project
6. Run `dotnet run`

N.B. If you leave `ClientId` and `Secret` blank when running the client, it will open a browser window with a login page.
This may be useful during initial setup and testing but is not recommended for production use.

</details>

## Important notes

### Time-to-live (TTL) = 3 days
Messages are stored in robust server-side queues, so it's not a problem if your connection is broken for a short while, but please note **messages have a time-to-live value of 3 days**. If you do not connect to IRIS for 3 days or more, some messages may have expired and no longer be available. In this case, it is possible to fill any data gaps using the APIs, given that they share the same output format.

### Receiving messages
**When you receive a message it will be removed from the queue and won't be available again via IRIS**. If you need to recover any data, you can use the API instead.

### Handling messages
**You don't need to write the messages to disk**. All of our example clients do, but you might consider directly integrating your messages into existing messaging services or processing them immediately in memory instead.

### One connection per queue
It is only possible to have **one connection per queue**. If you need multiple connections you can either share the message content from your client or consider setting up a separate IRIS queue.

### Message subject
The message subject of each message is the dataset name (e.g. `BOALF`).


## API documentation

IRIS and the Insight Solution APIs make available the same data, in the same output format, which enables you to use the [API documentation](https://developer.data.elexon.co.uk/) as a reference when using IRIS.

This interchangeability allows you to decide which data source works best for you or to use a combination of both.

## Tips on writing your own client

[Azure provides SDKs for building clients](https://learn.microsoft.com/en-us/azure/service-bus-messaging/). These are not strictly required, but they are definitely the easiest way to handle the authentication layer around AMQP.

Alongside your client credentials you will also need a `TenantId` to connect your own client to IRIS. This value is `1a235385-5d29-40e1-96fd-bc5ec2706361`.

We suggest looking at the example clients to get an understanding of how a client should work. Roughly each client is made up of:
  - **main client file** to pull together all the business logic
  - **service bus helper** to handle the AMQP authentication layer
  - **settings file** to store client credentials. It's important that this file is not checked into source control
  - **settings template file** to help other developers understand which credentials are required. This file can be safely checked in to source control
  - **message processor** to handle incoming IRIS messages
  - **error message processor** to gracefully handle any errors
  - **date format helper** to abstract away date string formatting logic (optional)

## Feedback
We're continuously making more data available through IRIS and further reducing latency. Help us improve the service by sharing your feedback to insightssupport@elexon.co.uk.

We also welcome contributions and suggestions directly to this repository. Please see our [contributing guidelines](./CONTRIBUTING.md) for more information.