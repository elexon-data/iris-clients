const serviceBusNamespace = process.env.SERVICE_BUS_NAMESPACE;
const queueName = process.env.QUEUE_NAME;
const downloadDirectory = process.env.RELATIVE_FILE_DOWNLOAD_DIRECTORY
const tenantId = "1a235385-5d29-40e1-96fd-bc5ec2706361"; // Elexon Tenant Id

if (!serviceBusNamespace) {
    throw new Error("Invalid configuration value: SERVICE_BUS_NAMESPACE is required");
}

if (!queueName) {
    throw new Error("Invalid configuration value: QUEUE_NAME is required");
}

if (!downloadDirectory) {
    throw new Error("Invalid configuration value: RELATIVE_FILE_DOWNLOAD_DIRECTORY is required");
}

if (!process.env.CLIENT_ID !== !process.env.SECRET) {
    throw new Error("Invalid configuration value(s): If one of CLIENT_ID and SECRET is provided, both are required")
}

const appRegistration =
  process.env.CLIENT_ID && process.env.SECRET
    ? {
        clientId: process.env.CLIENT_ID,
        secret: process.env.SECRET,
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
