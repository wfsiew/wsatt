from pony.orm import Database, db_session
from app.entities import Device

class DeviceService:
    
    @db_session
    @classmethod
    def findAllDevice(cls):
        return Device.select(o for o in Device)[:]
    
    @db_session
    @classmethod
    def insert(cls, serialNum: str, status: int):
        o = Device(serialNum=serialNum, status=status)
        
    @db_session
    @classmethod
    def selectByPrimaryKey(cls, id: int):
        return Device[id]
    
    @db_session
    @classmethod
    def selectDeviceBySerialNum(cls, serialNum: str):
        return Device.get(serialNum=serialNum)
    
    @db_session
    @classmethod
    def updateStatusByPrimaryKey(cls, id: int, status: int):
        o = Device[id]
        o.status = status
        