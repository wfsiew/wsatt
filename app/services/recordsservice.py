from pony.orm import Database, db_session
from app.entities import Records

class RecordsService:
    
    @db_session
    @classmethod
    def deleteByPrimaryKey(cls, id: int):
        Records[id].delete()
        
    @db_session
    @classmethod
    def insert(cls, record: Records):
        o = Records(
            enrollId=record.enrollId, 
            recordsTime=record.recordsTime, 
            mode=record.mode, 
            intout=record.intout, 
            event=record.event,
            deviceSerialNum=record.deviceSerialNum,
            temperature=record.temperature,
            image=record.image
        )
        
    @db_session
    @classmethod
    def insertSelective(cls, record: Records):
        cls.insert(record)
        
    @db_session
    @classmethod
    def selectByPrimaryKey(cls, id: int):
        return Records[id]
    
    @db_session
    @classmethod
    def updateByPrimaryKeySelective(cls, record: Records):
        cls.updateByPrimaryKey(record)
        
    @db_session
    @classmethod
    def updateByPrimaryKey(cls, record: Records):
        o = Records[record.id]
        o.enrollId = record.enrollId
        o.recordsTime = record.recordsTime
        o.mode = record.mode
        o.intout = record.intout
        o.event = record.event
        o.deviceSerialNum = record.deviceSerialNum
        o.temperature = record.temperature
        o.image = record.image
        
    @db_session
    @classmethod
    def selectAllRecords(cls):
        return Records.select(o for o in Records)[:]