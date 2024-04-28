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
    
@dataclass
class UserInfo:
    enrollId: int
    name: str
    backupnum: int
    admin: int
    imagePath: str
    record: str
    
    def __init__(self):
        pass
    
    def __str__(self):
        return f'UserInfo [enrollId={self.enrollId}, name={self.name}, backupnum={self.backupnum}, admin={self.admin}, imagePath={self.imagePath}, record={self.record}]'
    
@dataclass
class UserTemp:
    enrollId: int
    admin: int
    backupnum: int
    
    def __init__(self):
        pass
    
    def __str__(self):
        return f'UserTemp [enrollId={self.enrollId}, admin={self.admin}, backupnum={self.backupnum}]'
    
# with db_session:
#     author = Author(name='John Doe')
#     book = Book(title='Python Programming', publication_date='2022-01-01', isbn='978-0-123456-78-9', author=author)