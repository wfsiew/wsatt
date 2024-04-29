from pony.orm import Database, db_session
from app.entities import Person
from app.websocketpool import WebSocketPool

import time, json

class PersonService:
    
    @classmethod
    def updateByPrimaryKeySelective(cls, record: Person):
        cls.updateByPrimaryKey(record)
            
    @classmethod
    def updateByPrimaryKey(cls, record: Person):
        with db_session:
            o = Person[record.id]
            o.name = record.name
            o.rollId = record.rollId
            
    @classmethod
    def insertSelective(cls, person: Person):
        cls.insert(person)
            
    @classmethod
    def insert(cls, person: Person):
        with db_session:
            Person(name=person.name, rollId=person.rollId)
            
    @classmethod
    def deleteByPrimaryKey(cls, id: int):
        with db_session:
            Person[id].delete()
            
    @classmethod
    def selectByPrimaryKey(cls, id: int):
        with db_session:
            return Person[id]
        
    @classmethod
    def selectAll(cls) -> list[Person]:
        with db_session:
            return Person.select(o for o in Person)[:]
        
    @classmethod
    def setUserToDevice(cls, enrollId: int, name: str, backupnum: int, admin: int, records: str, deviceSn: str):
        time.sleep(0.4)
        x = {
            'cmd': 'setuserinfo',
            'enrollid': enrollId,
            'name': name,
            'backupnum': backupnum,
            'admin': admin,
            'record': records
        }
        ms = json.dumps(x)
        
        if backupnum in [10, 11]:
            pass
        
        deviceStatus1 = WebSocketPool.getDeviceStatus(deviceSn)
        if deviceStatus1.status == 1:
            deviceStatus1.status = 0
            WebSocketPool.addDeviceAndStatus(deviceSn, deviceStatus1)
            WebSocketPool.sendMessageToDeviceStatus(deviceSn, ms)
            
        else:
            time.sleep(0.6)
            deviceStatus1.status = 0
            WebSocketPool.addDeviceAndStatus(deviceSn, deviceStatus1)
            WebSocketPool.sendMessageToDeviceStatus(deviceSn, ms)
            
            