from pony.orm import *

db = Database()
db.bind(provider='sqlite', filename='../attdb.db', create_db=True)

class AccessDay(db.Entity):
    _table_ = 'access_day'
    id = PrimaryKey(int, auto=True)
    serial = Required(str)
    name = Required(str)
    startTime1 = Required(str)
    endTime1 = Required(str)
    startTime2 = Required(str)
    endTime2 = Required(str)
    startTime3 = Required(str)
    endTime3 = Required(str)
    startTime4 = Required(str)
    endTime4 = Required(str)
    startTime5 = Required(str)
    endTime5 = Required(str)
    
    def __str__(self):
        return f'''AccessDay [id={self.id}, serial={self.serial}, name={self.name} 
        , startTime1={self.startTime1}, endTime1={self.endTime1}
        , startTime2={self.startTime2}, endTime1={self.endTime2}
        , startTime3={self.startTime3}, endTime1={self.endTime3}
        , startTime4={self.startTime1}, endTime4={self.endTime4}
        , startTime5={self.startTime5}, endTime1={self.endTime5}]'''
        
class AccessWeek(db.Entity):
    _table_ = 'access_week'
    id = PrimaryKey(int, auto=True)
    serial = Required(str)
    name = Required(str)
    sunday = Required(int)
    monday = Required(int)
    tuesday = Required(int)
    wednesday = Required(int)
    thursday = Required(int)
    friday = Required(int)
    saturday = Required(int)
    
    def __str__(self):
        return f'''AccessWeek [id={self.id}, serial={self.serial}, name={self.name}
        , monday={self.monday}, tuesday={self.tuesday}
        , wednesday={self.wednesday}, thursday={self.thursday}
        , friday={self.friday}, saturday={self.saturday}, sunday={self.sunday}]'''

class Device(db.Entity):
    _table_ = 'device'
    id = PrimaryKey(int, auto=True)
    serialNum = Required(str)
    status = Required(int)
    
    def __str__(self):
        return f'Device [id={self.id}, serialNum={self.serialNum}, status={self.status}]'
    
class EnrollInfo(db.Entity):
    _table_ = 'enrollinfo'
    id = PrimaryKey(int, auto=True)
    enrollId = Required(int)
    backupnum = Required(int)
    imagePath = Required(str)
    signatures = Required(str)
    
    def __str__(self):
        return f'EnrollInfo [id={self.id}, enrollId={self.enrollId}, backupnum={self.backupnum}, imagePath={self.imagePath}, signatures={self.signatures}]'
    
class Person(db.Entity):
    _table_ = 'person'
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    rollId = Required(int)
    
    def __str__(self):
        return f'Person [id={self.id}, name={self.name}, rollId={self.rollId}]'
    
class Records(db.Entity):
    _table_ = 'records'
    id = PrimaryKey(int, auto=True)
    enrollId = Required(int)
    recordsTime = Required(str)
    mode = Required(int)
    intout = Required(int)
    event = Required(int)
    deviceSerialNum = Required(str)
    temperature = Required(float)
    image = Required(str)
    
db.generate_mapping(create_tables=True)