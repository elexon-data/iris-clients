namespace IrisClient;

public sealed class AppRegistration
{
    public string? ClientId { get; set; }
    public string? Secret { get; set; }
}

public sealed class Settings
{
    public string TenantId = "1a235385-5d29-40e1-96fd-bc5ec2706361"; // Elexon Tenant Id
    public string? ServiceBusNamespace { get; set; }
    public string FullyQualifiedNamespace => $"{ServiceBusNamespace}.servicebus.windows.net";
    public string? ServiceBusQueue { get; set; }
    public string? RelativeFileDownloadDirectory { get; set; }
    public AppRegistration? AppRegistration { get; set; }

    public bool IsAppRegistrationProvided()
    {
        if (AppRegistration == null)
        {
            return false;
        }

        return !string.IsNullOrWhiteSpace(AppRegistration.ClientId) &&
               !string.IsNullOrWhiteSpace(AppRegistration.Secret);
    }

    public void Validate()
    {
        if (string.IsNullOrWhiteSpace(ServiceBusQueue))
        {
            throw new SystemException($"Invalid configuration value: {nameof(ServiceBusQueue)} is required");
        }

        if (string.IsNullOrWhiteSpace(ServiceBusNamespace))
        {
            throw new SystemException($"Invalid configuration value: {nameof(ServiceBusNamespace)} is required");
        }

        if (string.IsNullOrWhiteSpace(ServiceBusQueue))
        {
            throw new SystemException($"Invalid configuration value: {nameof(ServiceBusQueue)} is required");
        }
        
        if (string.IsNullOrWhiteSpace(RelativeFileDownloadDirectory))
        {
            throw new SystemException($"Invalid configuration value: {nameof(RelativeFileDownloadDirectory)} is required");
        }

        if (AppRegistration != null)
        {
            if (string.IsNullOrWhiteSpace(AppRegistration.ClientId) !=
                string.IsNullOrWhiteSpace(AppRegistration.Secret))
            {
                throw new SystemException(
                    $"Invalid configuration value(s): If {nameof(AppRegistration)} is provided, " +
                    $"{nameof(AppRegistration.ClientId)} and " +
                    $"{nameof(AppRegistration.Secret)} are both required.");
            }
        }
    }
}