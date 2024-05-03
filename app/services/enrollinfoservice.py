from typing import List
from pony.orm import db_session
from app.entities import EnrollInfo
from app.models import UserInfo

import app.services.personservice as pe

class EnrollInfoService:
    
    @classmethod
    def deleteByPrimaryKey(cls, id: int):
        with db_session:
            EnrollInfo[id].delete()
            
    @classmethod
    def insertSelective(cls, records: List[EnrollInfo]):
        with db_session:
            for record in records:
                EnrollInfo(enrollId=record.enrollId, backupnum=record.backupnum, imagePath=record.imagePath, signatures=record.signatures)
            
    @classmethod
    def selectByPrimaryKey(cls, id: int):
        with db_session:
            return EnrollInfo.get(id=id)
        
    @classmethod
    def updateByPrimaryKeySelective(cls, record: EnrollInfo):
        with db_session:
            o = EnrollInfo[record.id]
            o.enrollId = record.enrollId
            o.backupnum = record.backupnum
            o.imagePath = record.imagePath
            o.signatures = record.signatures
            
    @classmethod
    def updateByPrimaryKeyWithBLOBs(cls, record: EnrollInfo):
        cls.updateByPrimaryKeySelective(record)
            
    @classmethod
    def insert(cls, enrollid: int, backupnum: int, imagePath: str, signature: str):
        with db_session:
            EnrollInfo(enrollId=enrollid, backupnum=backupnum, imagePath=imagePath, signatures=signature)
            
    @classmethod
    def selectByBackupnum(cls, enrollId: int, backupnum: int) -> EnrollInfo:
        with db_session:
            return EnrollInfo.get(enrollId=enrollId, backupnum=backupnum)
        
    @classmethod
    def usersToSendDevice(cls):
        persons = pe.PersonService.selectAll()
        enrollInfos = cls.selectAll()
        userInfos: List[UserInfo] = []
        
        for p in persons:
            for e in enrollInfos:
                if p.id == e.enrollId:
                    userInfo = UserInfo()
                    userInfo.admin = p.rollId
                    userInfo.backupnum = e.backupnum
                    userInfo.enrollId = p.id
                    userInfo.name = p.name
                    userInfo.record = e.signatures
                    
                    userInfos.append(userInfo)
                    
        return userInfos
        
    @classmethod
    def selectAll(cls) -> List[EnrollInfo]:
        with db_session:
            return EnrollInfo.select()[:]
        
    @classmethod
    def selectByEnrollId(cls, enrollId: int) -> List[EnrollInfo]:
        with db_session:
            return EnrollInfo.select(lambda o: o.enrollId == enrollId)[:]
        
    @classmethod
    def updateByEnrollIdAndBackupNum(cls, signatures: str, enrollId: int, backupnum: int):
        with db_session:
            q = EnrollInfo.select(lambda o: o.enrollId == enrollId and o.backupnum == backupnum)[:]
            for o in q:
                o.signatures = signatures