from tortoise import connections
from tortoise.transactions import in_transaction
from app.entities import Device

class DeviceService:
    
    @classmethod
    async def findAllDevice(cls):
        return await Device.all()
    
    @classmethod
    async def insert(cls, serialNum: str, status: int):
        await Device.create(serialNum=serialNum, status=status)

    @classmethod
    async def selectByPrimaryKey(cls, id: int):
        return await Device.get_or_none(id=id)
    
    @classmethod
    async def selectDeviceBySerialNum(cls, serialNum: str):
        return await Device.get_or_none(serialNum=serialNum)
    
    @classmethod
    async def updateStatusByPrimaryKey(cls, id: int, status: int):
        await Device.filter(id=id).update(status=status)