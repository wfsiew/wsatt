from websocket_server import WebsocketServer
from dataclasses import dataclass
from pony.orm import *

db = Database()
db.bind(provider='sqlite', filename='../attdb.db', create_db=True)

class Author(db.Entity):
    name = Required(str)
    books = Set('Book')

class Book(db.Entity):
    title = Required(str)
    publication_date = Required(str)
    isbn = Required(str)
    author = Required(Author)
    
db.generate_mapping(create_tables=True)

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
    
# with db_session:
#     author = Author(name='John Doe')
#     book = Book(title='Python Programming', publication_date='2022-01-01', isbn='978-0-123456-78-9', author=author)