from websocket_server import WebsocketServer
from dataclasses import dataclass

@dataclass
class DeviceStatus:
    deviceSn: str
    webSocket: WebsocketServer
    client: any
    status: int
    
    def __init__(self):
        pass
    
    def __str__(self):
        return f'DeviceStatus [deviceSn={self.deviceSn}, webSocket={self.webSocket}, status={self.status}]'