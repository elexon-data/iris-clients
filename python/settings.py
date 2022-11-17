from dataclasses import dataclass, field

@dataclass
class SettingsAppRegistration:
    ClientId: str
    Secret: str

@dataclass
class Settings:
    TenantId = "1a235385-5d29-40e1-96fd-bc5ec2706361"
    ServiceBusNamespace: str
    FullyQualifiedNamespace: str = field(init=False)
    ServiceBusQueue:str
    
    RelativeFileDownloadDirectory: str
    AppRegistration: SettingsAppRegistration

    def __post_init__(self):
        self.FullyQualifiedNamespace = f"{self.ServiceBusNamespace}.servicebus.windows.net";