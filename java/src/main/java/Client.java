
import com.azure.identity.ClientSecretCredential;
import com.azure.identity.ClientSecretCredentialBuilder;
import com.azure.messaging.servicebus.ServiceBusClientBuilder;
import com.azure.messaging.servicebus.ServiceBusErrorContext;
import com.azure.messaging.servicebus.ServiceBusReceivedMessageContext;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class Client {

    public void start() {

        var credential = createCredential();

        var processor = new ServiceBusClientBuilder()
                .fullyQualifiedNamespace(Settings.getNameSpace())
                .credential(credential)
                .processor()
                .queueName(Settings.getQueueName())
                .processMessage(this::processMessage)
                .processError(this::processError)
                .buildProcessorClient();

        processor.start();

    }

    private ClientSecretCredential createCredential() {
        return new ClientSecretCredentialBuilder()
                .tenantId(Settings.getTenantId())
                .clientId(Settings.getClientId())
                .clientSecret(Settings.getSecret())
                .build();
    }

    private void processMessage(ServiceBusReceivedMessageContext context) {
        writeMessage(context.getMessage().getBody().toString());
    }

    private void processError(ServiceBusErrorContext context) {
        writeMessage(context.getException().getMessage());
    }

    private void writeMessage(String message) {
        try {
            System.out.println("writing message in data file");
            var path = getDownloadFilePath();
            Files.writeString(path, message, StandardOpenOption.APPEND);
        } catch (Exception ex) {
            System.err.println(ex.getMessage());
        }
    }

    private Path getDownloadFilePath() throws IOException {
        var path = Path.of(Settings.getDownloadFilePath());
        if (!Files.exists(path)) {
            Files.createFile(path);
        }
        return path;
    }

}