from typing import List
from tortoise import connections
from tortoise.transactions import in_transaction
from app.entities import Person, PersonModel
from app.websocketpool import WebSocketPool

import app.services.enrollinfoservice as en
import time, json

class PersonService:
    
    @classmethod
    async def updateByPrimaryKeySelective(cls, record: Person):
        await cls.updateByPrimaryKey(record)
            
    @classmethod
    async def updateByPrimaryKey(cls, record: Person):
        await Person.filter(id=record.id).update(name=record.name, rollId=record.rollId)
            
    @classmethod
    async def insertSelective(cls, person: PersonModel):
        await cls.insert([person])
            
    @classmethod
    async def insert(cls, persons: List[PersonModel]):
        for person in persons:
            await Person.create(name=person.name, rollId=person.rollId)
            
    @classmethod
    async def deleteByPrimaryKey(cls, id: int):
        await Person.filter(id=id).delete()
            
    @classmethod
    async def selectByPrimaryKey(cls, id: int):
        return await Person.get_or_none(id=id)
        
    @classmethod
    async def selectAll(cls):
        return await Person.all()
    
    @classmethod
    async def selectAllId(cls):
        return await Person.all().values_list('id', flat=True)
        
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
    async def setUserToDevice2(cls, deviceSn: str):
        userInfos = await en.EnrollInfoService.usersToSendDevice()
        
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
    async def setUsernameToDevice(cls, deviceSn: str):
        persons = await cls.selectAll()
        
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