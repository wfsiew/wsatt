from typing import List
from pony.orm import Database, db_session
from app.entities import Person, PersonModel
from app.websocketpool import WebSocketPool

import app.services.enrollinfoservice as en
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
    def insertSelective(cls, person: PersonModel):
        cls.insert([person])
            
    @classmethod
    def insert(cls, persons: List[PersonModel]):
        with db_session:
            for person in persons:
                Person(name=person.name, rollId=person.rollId)
            
    @classmethod
    def deleteByPrimaryKey(cls, id: int):
        with db_session:
            Person[id].delete()
            
    @classmethod
    def selectByPrimaryKey(cls, id: int):
        with db_session:
            return Person.get(id=id)
        
    @classmethod
    def selectAll(cls) -> List[Person]:
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
            
    @classmethod
    def setUserToDevice2(cls, deviceSn: str):
        userInfos = en.EnrollInfoService.usersToSendDevice()
        
        for o in userInfos:
            enrollId = o.enrollId
            name = o.name
            backupnum = o.backupnum
            admin = o.admin
            record = o.record
            time.sleep(0.1)
            x = {
                'cmd': 'setuserinfo',
                'enrollid': enrollId,
                'name': name,
                'backupnum': backupnum,
                'admin': admin,
                'record': record
            }
            ms = json.dumps(x)
            
            if backupnum in [10, 11]:
                pass
            
            deviceStatus1 = WebSocketPool.getDeviceStatus(deviceSn)
            if deviceStatus1.status == 1:
                deviceStatus1.status = 0
                WebSocketPool.addDeviceAndStatus(deviceSn, deviceStatus1)
                WebSocketPool.sendMessageToDeviceStatus(deviceSn, ms)