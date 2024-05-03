from typing import List
from pony.orm import db_session
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
            return Person.select()
        
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
                
    @classmethod
    def deleteUserInfoFromDevice(cls, enrollId: int, deviceSn: str):
        i = 0
        time.sleep(0.01)
        backupnum = 13
        m = {
            'cmd': 'deleteuser',
            'enrollid': enrollId,
            'backupnum': backupnum
        }
        ms = json.dumps(m)
        deviceStatus = WebSocketPool.getDeviceStatus(deviceSn)
        if deviceStatus.status == 1:
            deviceStatus.status = 0
            WebSocketPool.addDeviceAndStatus(deviceSn, deviceStatus)
            if deviceStatus.webSocket is not None:
                WebSocketPool.sendMessageToDeviceStatus(deviceSn, ms)
                i = i + 1
                
    @classmethod
    def setUsernameToDevice(cls, deviceSn: str):
        with db_session:
            persons = cls.selectAll()
            
            m = {
                'cmd': 'setusername',
                'count': len(persons)
            }
            records = []
            for o in persons:
                s = {
                    'enrollid': o.id,
                    'name': o.name,
                }
                records.append(s)
                
            m['record'] = records
            ms = json.dumps(m)
            i = 0
            while i < 1:
                deviceStatus = WebSocketPool.getDeviceStatus(deviceSn)
                if deviceStatus.status == 1:
                    deviceStatus.status = 0
                    WebSocketPool.addDeviceAndStatus(deviceSn, deviceStatus)
                    if deviceStatus.webSocket is not None:
                        WebSocketPool.sendMessageToDeviceStatus(deviceSn, ms)
                        i = i + 1