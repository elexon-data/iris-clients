import java.io.IOException;
import java.io.InputStream;
import java.util.Objects;
import java.util.Properties;

public final class Settings {

    private static final String SETTINGS_FILE = "settings_template.properties";
    private static final String TENANT_ID_KEY = "TENANT_ID";
    private static final String CLIENT_ID_KEY = "CLIENT_ID";
    private static final String SECRET_KEY = "SECRET";
    private static final String QUEUE_NAME_KEY = "QUEUE_NAME";
    private static final String FULLY_QUALIFIED_NAMESPACE = "FULLY_QUALIFIED_NAMESPACE";
    private static final String DOWNLOAD_FILE_PATH_DIR = "DOWNLOAD_FILE_PATH_DIR";

    private static final Properties PROPERTIES;

    static {
        try (InputStream is = Settings.class.getResourceAsStream(SETTINGS_FILE)) {
            Objects.requireNonNull(is, "Settings file not found");
            PROPERTIES = new Properties();
            PROPERTIES.load(is);
        } catch (IOException e) {
            throw new RuntimeException("Failed to load settings", e);
        }
    }

    private Settings() {}

    public static String getTenantId() {
        return PROPERTIES.getProperty(TENANT_ID_KEY);
    }

    public static String getClientId() {
        return PROPERTIES.getProperty(CLIENT_ID_KEY);
    }

    public static String getSecret() {
        return PROPERTIES.getProperty(SECRET_KEY);
    }

    public static String getQueueName() {
        return PROPERTIES.getProperty(QUEUE_NAME_KEY);
    }

    public static String getFullyQualifiedNamespace() {
        return PROPERTIES.getProperty(FULLY_QUALIFIED_NAMESPACE);
    }

    public static String getDownloadFilePathDir() {
        return PROPERTIES.getProperty(DOWNLOAD_FILE_PATH_DIR);
    }

}