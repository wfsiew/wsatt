from typing import List
from pony.orm import db_session
from app.entities import Device

class DeviceService:
    
    @classmethod
    def findAllDevice(cls) -> List[Device]:
        with db_session:
            return Device.select(o for o in Device)[:]
    
    @classmethod
    def insert(cls, serialNum: str, status: int):
        with db_session:
            Device(serialNum=serialNum, status=status)

    @classmethod
    def selectByPrimaryKey(cls, id: int):
        with db_session:
            return Device.get(id=id)
    
    @classmethod
    def selectDeviceBySerialNum(cls, serialNum: str) -> Device:
        with db_session:
            return Device.get(serialNum=serialNum)
    
    @classmethod
    def updateStatusByPrimaryKey(cls, id: int, status: int):
        with db_session:
            o = Device.get(id=id)
            o.status = status
        