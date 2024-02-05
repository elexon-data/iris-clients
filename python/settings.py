from dataclasses import dataclass, field


@dataclass
class Settings:
    TenantId = "1a235385-5d29-40e1-96fd-bc5ec2706361"
    ServiceBusNamespace: str
    FullyQualifiedNamespace: str = field(init=False)
    QueueName: str
    ClientId: str
    Secret: str

    RelativeFileDownloadDirectory: str

    def __post_init__(self):
        self.FullyQualifiedNamespace = (
            f"{self.ServiceBusNamespace}.servicebus.windows.net"
        )
        if not self.ServiceBusNamespace:
            raise ValueError(
                "Invalid configuration value: ServiceBusNamespace is required"
            )
        if not self.QueueName:
            raise ValueError("Invalid configuration value: QueueName is required")
        if not self.RelativeFileDownloadDirectory:
            raise ValueError(
                "Invalid configuration value: RelativeFileDownloadDirectory is required"
            )
        if bool(self.ClientId) != bool(self.Secret):
            raise ValueError(
                "Invalid configuration value(s): If one of ClientId and Secret are provided, both are required"
            )
