from pony.orm import Database, db_session
from app.entities import Records

class RecordsService:
    
    @classmethod
    def deleteByPrimaryKey(cls, id: int):
        with db_session:
            Records[id].delete()
        
    # @classmethod
    # def insert(cls, record: Records):
    #     with db_session:
    #         Records(
    #             enrollId=record.enrollId, 
    #             recordsTime=record.recordsTime, 
    #             mode=record.mode, 
    #             intout=record.intout, 
    #             event=record.event,
    #             deviceSerialNum=record.deviceSerialNum,
    #             temperature=record.temperature,
    #             image=record.image
    #         )

    # @classmethod
    # def insertSelective(cls, record: Records):
    #     cls.insert(record)
        
    @classmethod
    def selectByPrimaryKey(cls, id: int):
        with db_session:
            return Records.get(id=id)
    
    @classmethod
    def updateByPrimaryKeySelective(cls, record: Records):
        cls.updateByPrimaryKey(record)
        
    @classmethod
    def updateByPrimaryKey(cls, record: Records):
        with db_session:
            o = Records[record.id]
            o.enrollId = record.enrollId
            o.recordsTime = record.recordsTime
            o.mode = record.mode
            o.intout = record.intout
            o.event = record.event
            o.deviceSerialNum = record.deviceSerialNum
            o.temperature = record.temperature
            o.image = record.image

    @classmethod
    def selectAllRecords(cls) -> list[Records]:
        with db_session:
            return Records.select(o for o in Records)[:]