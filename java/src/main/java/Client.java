import com.azure.identity.ClientSecretCredential;
import com.azure.identity.ClientSecretCredentialBuilder;
import com.azure.messaging.servicebus.ServiceBusClientBuilder;
import com.azure.messaging.servicebus.ServiceBusErrorContext;
import com.azure.messaging.servicebus.ServiceBusReceivedMessage;
import com.azure.messaging.servicebus.ServiceBusReceivedMessageContext;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.time.LocalDateTime;

public class Client {

    public void start() {

        var credential = createCredential();

        var processor = new ServiceBusClientBuilder()
                .fullyQualifiedNamespace(Settings.getFullyQualifiedNamespace())
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
        writeMessage(context.getMessage());
    }

    private void processError(ServiceBusErrorContext context) {
        System.err.println(context.getException().getMessage());
    }

    private void writeMessage(ServiceBusReceivedMessage message) {
        try {
            var fileName = message.getSubject() + LocalDateTime.now();
            System.out.println("writing message in file: " + fileName);
            var path = getDownloadFilePath(fileName);
            Files.writeString(path, message.getBody().toString(), StandardOpenOption.APPEND);
        } catch (Exception ex) {
            System.err.println(ex.getMessage());
        }
    }

    private Path getDownloadFilePath(String fileName) throws IOException {
        var path = Path.of(Settings.getDownloadFilePathDir().concat(File.separator).concat(fileName));
        Files.createDirectories(path.getParent());
        if (!Files.exists(path)) {
            Files.createFile(path);
        }
        return path;
    }

}