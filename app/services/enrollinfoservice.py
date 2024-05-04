from typing import List
from tortoise import connections
from tortoise.transactions import in_transaction
from app.entities import EnrollInfo, EnrollInfoModel
from app.models import UserInfo

import app.services.personservice as pe

class EnrollInfoService:
    
    @classmethod
    async def deleteByPrimaryKey(cls, id: int):
        await EnrollInfo.filter(id=id).delete()
            
    @classmethod
    async def insertSelective(cls, records: List[EnrollInfoModel]):
        for record in records:
            await EnrollInfo.create(enrollId=record.enrollId, backupnum=record.backupnum, imagePath=record.imagePath, signatures=record.signatures)
            
    @classmethod
    async def selectByPrimaryKey(cls, id: int):
        return await EnrollInfo.get_or_none(id=id)
        
    @classmethod
    async def updateByPrimaryKeySelective(cls, record: EnrollInfo):
        await EnrollInfo.filter(id=record.id).update(
            enrollId=record.enrollId,
            backupnum=record.backupnum,
            imagePath=record.imagePath,
            signatures=record.signatures
        )
            
    @classmethod
    async def updateByPrimaryKeyWithBLOBs(cls, record: EnrollInfo):
        await cls.updateByPrimaryKeySelective(record)
            
    @classmethod
    async def insert(cls, enrollid: int, backupnum: int, imagePath: str, signature: str):
        await EnrollInfo.create(enrollId=enrollid, backupnum=backupnum, imagePath=imagePath, signatures=signature)
            
    @classmethod
    async def selectByBackupnum(cls, enrollId: int, backupnum: int):
        return await EnrollInfo.get_or_none(enrollId=enrollId, backupnum=backupnum)
        
    @classmethod
    async def usersToSendDevice(cls):
        persons = await pe.PersonService.selectAll()
        lenrollid = [o.id for o in persons]
        enrollInfos = await cls.selectAllByEnrollId(lenrollid)
        userInfos: List[UserInfo] = []
        
        for p in persons:
            for e in enrollInfos:
                userInfo = UserInfo()
                userInfo.admin = p.rollId
                userInfo.backupnum = e.backupnum
                userInfo.enrollId = p.id
                userInfo.name = p.name
                userInfo.record = e.signatures
                
                userInfos.append(userInfo)
                    
        return userInfos
    
    @classmethod
    async def selectAllByEnrollId(cls, lenrollid: List[int]):
        return await EnrollInfo.filter(enrollId__in=lenrollid)
        
    @classmethod
    async def selectAll(cls):
        return await EnrollInfo.all()
        
    @classmethod
    async def selectByEnrollId(cls, enrollId: int):
        return await EnrollInfo.filter(enrollId=enrollId)
        
    @classmethod
    async def updateByEnrollIdAndBackupNum(cls, signatures: str, enrollId: int, backupnum: int):
        await EnrollInfo.filter(enrollId=enrollId, backupnum=backupnum).update(signatures=signatures)