using Azure.Identity;
using Azure.Messaging.ServiceBus;

namespace IrisClient.helpers;

public static class ServiceBusClientHelpers
{
    public static ServiceBusClient GetAuthenticatedServiceBusClient(
        Settings settings)
    {
        if (settings.IsAppRegistrationProvided())
        {
            var tokenCredential = new ClientSecretCredential(
                settings.TenantId,
                settings.AppRegistration!.ClientId,
                settings.AppRegistration.Secret);
            Console.WriteLine("Connecting using app registration");
            return new ServiceBusClient(settings.FullyQualifiedNamespace, tokenCredential);
        }

        Console.WriteLine("No connection string or app registration details found");
        Console.ForegroundColor = ConsoleColor.Yellow;
        Console.WriteLine("Login required to listen to queue");
        Console.ResetColor();

        var options = new InteractiveBrowserCredentialOptions
        {
            TenantId = settings.TenantId
        };
        var browserCredential = new InteractiveBrowserCredential(options);
        return new ServiceBusClient(settings.FullyQualifiedNamespace, browserCredential);
    }
}