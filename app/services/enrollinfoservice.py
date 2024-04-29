from pony.orm import Database, db_session
from app.entities import EnrollInfo
from app.models import UserInfo
from services.personservice import PersonService

class EnrollInfoService:
    
    @classmethod
    def deleteByPrimaryKey(cls, id: int):
        with db_session:
            EnrollInfo[id].delete()
            
    @classmethod
    def insertSelective(cls, record: EnrollInfo):
        with db_session:
            EnrollInfo(enrollId=record.enrollId, backupnum=record.backupnum, imagePath=record.imagePath, signatures=record.signatures)
            
    @classmethod
    def selectByPrimaryKey(cls, id: int):
        with db_session:
            return EnrollInfo[id]
        
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
    def selectByBackupnum(cls, enrollId: int, backupnum: int) -> list[EnrollInfo]:
        with db_session:
            return EnrollInfo.select(lambda o: o.enrollId == enrollId and o.backupnum == backupnum).first()
        
    @classmethod
    def usersToSendDevice(cls):
        persons = PersonService.selectAll()
        enrollInfos = cls.selectAll()
        userInfos: list[UserInfo] = []
        
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
    def selectAll(cls) -> list[EnrollInfo]:
        with db_session:
            return EnrollInfo.select(o for o in EnrollInfo)[:]
        
    @classmethod
    def selectByEnrollId(cls, enrollId: int) -> list[EnrollInfo]:
        with db_session:
            return EnrollInfo.select(lambda o: o.enrollId == enrollId)[:]
        
    @classmethod
    def updateByEnrollIdAndBackupNum(cls, signatures: str, enrollId: int, backupnum: int):
        with db_session:
            for o in EnrollInfo.select(lambda o: o.enrollId == enrollId and o.backupnum == backupnum):
                o.signatures = signatures