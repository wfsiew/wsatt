from pony.orm import Database, db_session
from app.entities import Device

class DeviceService:
    
    @db_session
    @classmethod
    def findAllDevice(cls):
        return Device.select(o for o in Device)[:]
    
    @classmethod
    def insert(cls, serialNum: str, status: int):
        with db_session:
            Device(serialNum=serialNum, status=status)
        
    @db_session
    @classmethod
    def selectByPrimaryKey(cls, id: int):
        return Device[id]
    
    @classmethod
    def selectDeviceBySerialNum(cls, serialNum: str):
        with db_session:
            return Device.get(serialNum=serialNum)
    
    @classmethod
    def updateStatusByPrimaryKey(cls, id: int, status: int):
        with db_session:
            o = Device[id]
            o.status = status
        