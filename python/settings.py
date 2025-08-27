from dataclasses import dataclass, field
import sys


@dataclass
class Settings:
    TenantId = "4203b7a0-7773-4de5-b830-8b263a20426e"
    ServiceBusNamespace: str
    FullyQualifiedNamespace: str = field(init=False)
    QueueName: str
    ClientId: str
    Secret: str

    RelativeFileDownloadDirectory: str

    def __post_init__(self):
        self.FullyQualifiedNamespace = f"{self.ServiceBusNamespace}.servicebus.windows.net";
        if not self.ServiceBusNamespace:
            sys.exit('Invalid configuration value: ServiceBusNamespace is required')
        if not self.QueueName:
            sys.exit('Invalid configuration value: QueueName is required')
        if not self.RelativeFileDownloadDirectory:
            sys.exit('Invalid configuration value: RelativeFileDownloadDirectory is required')
        if bool(self.ClientId) is not bool(self.Secret):
            sys.exit('Invalid configuration value(s): If one of ClientId and Secret are provided, both are required')
