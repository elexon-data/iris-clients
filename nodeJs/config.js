const serviceBusNamespace = process.env.SERVICE_BUS_NAMESPACE;
const queueName = process.env.SERVICE_BUS_QUEUE;
const downloadDirectory = process.env.RELATIVE_FILE_DOWNLOAD_DIRECTORY
const tenantId = "1a235385-5d29-40e1-96fd-bc5ec2706361"; // Elexon Tenant Id

const isEmptyOrSpaces = (string) => {
    return string === null || string.match(/^\s*$/) !== null;
}

if (isEmptyOrSpaces(serviceBusNamespace)) {
    throw new Error("Invalid configuration value: SERVICE_BUS_NAMESPACE is required");
}

if (isEmptyOrSpaces(queueName)) {
    throw new Error("Invalid configuration value: SERVICE_BUS_QUEUE is required");
}

if (isEmptyOrSpaces(downloadDirectory)) {
    throw new Error("Invalid configuration value: RELATIVE_FILE_DOWNLOAD_DIRECTORY is required");
}

const appRegistration =
  process.env.APP_REGISTRATION_CLIENT_ID && process.env.APP_REGISTRATION_SECRET
    ? {
        clientId: process.env.APP_REGISTRATION_CLIENT_ID,
        secret: process.env.APP_REGISTRATION_SECRET,
      }
    : null;

const fullyQualifiedNamespace = `${serviceBusNamespace}.servicebus.windows.net`;

export default {
  serviceBusNamespace,
  fullyQualifiedNamespace,
  queueName,
  tenantId,
  appRegistration, 
  downloadDirectory,
};
