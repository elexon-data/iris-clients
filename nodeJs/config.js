const serviceBusNamespace = process.env.SERVICE_BUS_NAMESPACE;
const queueName = process.env.SERVICE_BUS_QUEUE;
const tenantId = "1a235385-5d29-40e1-96fd-bc5ec2706361"; // Elexon Tenant Id

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
};
