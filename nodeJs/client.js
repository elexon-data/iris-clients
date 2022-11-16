import { ServiceBusClient } from "@azure/service-bus";
import {
  ClientSecretCredential,
  InteractiveBrowserCredential,
} from "@azure/identity";
import { processMessage } from "./processors/processMessage.js";
import { processError } from "./processors/processError.js";
import config from "./config.js";

const main = async () => {
  let credential;

  if (config.appRegistration) {
    credential = new ClientSecretCredential(
      config.tenantId,
      config.appRegistration.clientId,
      config.appRegistration.secret
    );
  } else {
    credential = new InteractiveBrowserCredential({
      tenantId: config.tenantId,
      redirectUri: "http://localhost:1337",
    });
  }

  const serviceBusClient = new ServiceBusClient(
    config.fullyQualifiedNamespace,
    credential
  );
  const receiver = serviceBusClient.createReceiver(config.queueName);

  console.log("Initiating connection. Details:", {
    serviceBusNamespace: config.serviceBusNamespace,
    queueName: config.queueName,
  });

  receiver.subscribe({
    processMessage,
    processError,
  });
};

main().catch((err) => {
  console.log("Error occurred: ", err);
  process.exit(1);
});
