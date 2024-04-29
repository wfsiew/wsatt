from typing import List
from websocket_server import WebsocketServer
from pony.orm import db_session
from datetime import datetime
import logging, json, traceback

from app.models import DeviceStatus, UserTemp
from app.entities import *
from app.services.deviceservice import DeviceService
from app.services.recordsservice import RecordsService
from app.websocketpool import WebSocketPool
from app import utils

import app.services.personservice as pe
import app.services.enrollinfoservice as en

logger = utils.getLogger('main')

def getDeviceInfo(cli, server, m):
    sn = m.get('sn')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if sn is not None:
        d1 = DeviceService.selectDeviceBySerialNum(sn)
        if d1 is None:
            DeviceService.insert(sn, 1)
            
        else:
            DeviceService.updateStatusByPrimaryKey(d1.id, 1)
            
        x = {
            'ret': 'reg',
            'result': True,
            'cloudtime': now
        }
        ms = json.dumps(x)
        WebSocketPool.sendMessageToDevice(cli, server, ms)
        deviceStatus = DeviceStatus()
        deviceStatus.deviceSn = sn
        deviceStatus.status = 1
        deviceStatus.webSocket = server
        deviceStatus.client = cli
        WebSocketPool.addDeviceAndStatus(sn, deviceStatus)
            
    else:
        x = {
            'ret': 'reg',
            'result': False,
            'reason': 1
        }
        ms = json.dumps(x)
        WebSocketPool.sendMessageToDevice(cli, server, ms)
        
def getAttandence(cli, server, m):
    sn = m.get('sn')
    count = int(m.get('count', 0))
    logindex = int(m.get('logindex', -1))
    records = m.get('record', [])
    # recordAll: List[Records] = []
    deviceStatus = DeviceStatus()
    
    if count > 0:
        with db_session:
            for o in records:
                enrollid = int(o.get('enrollid', 0))
                time = o.get('time')
                mode = int(o.get('mode', 0))
                inout = int(o.get('inout', 0))
                event = int(o.get('event', 0))
                temperature = 0
                
                if o.get('temp') is not None:
                    temperature = float(o.get('temp', 0))
                    temperature = temperature / 100.0
                    temperature = round(temperature * 10) / 10.0
                    
                Records(deviceSerialNum=sn, enrollId=enrollid, event=event, intout=inout, mode=mode, recordsTime=time, temperature=temperature, image=o.get('image'))
                
                # if o.get('image') is not None:
                #     record.image = o.get('image')
                    
                # recordAll.append(record)
            
        if logindex >= 0:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            x = {
                'ret': 'sendlog',
                'result': True,
                'count': count,
                'logindex': logindex,
                'cloudtime': now
            }
            ms = json.dumps(x)
            WebSocketPool.sendMessageToDevice(cli, server, ms)
            
        elif logindex < 0:
            x = {
                'ret': 'sendlog',
                'result': True,
                'cloudtime': now
            }
            ms = json.dumps(x)
            WebSocketPool.sendMessageToDevice(cli, server, ms)
            
        deviceStatus.deviceSn = sn
        deviceStatus.status = 1
        deviceStatus.webSocket = server
        deviceStatus.client = cli
        WebSocketPool.addDeviceAndStatus(sn, deviceStatus)
        
    elif count == 0:
        x = {
            'ret': 'sendlog',
            'result': False,
            'reason': 1
        }
        ms = json.dumps(x)
        WebSocketPool.sendMessageToDevice(cli, server, ms)
        deviceStatus.deviceSn = sn
        deviceStatus.status = 1
        deviceStatus.webSocket = server
        deviceStatus.client = cli
        WebSocketPool.addDeviceAndStatus(sn, deviceStatus)
        
    # for recordsTemp in recordAll:
    #     RecordsService.insert(recordsTemp)
        
def getEnrollInfo(cli, server, m):
    sn = m.get('sn')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sn = m.get('sn')
    signatures1 = m.get('record')
    deviceStatus = DeviceStatus()
    
    if signatures1 is None:
        x = {
            'ret': 'senduser',
            'result': False,
            'reason': 1
        }
        ms = json.dumps(x)
        WebSocketPool.sendMessageToDevice(cli, server, ms)
        WebSocketPool.addDeviceAndStatus(sn, deviceStatus)
        
    else:
        backupnum = int(m.get('backupnum', 0))
        enrollId = int(m.get('enrollId', 0))
        name = m.get('name')
        rollId = int(m.get('admin', 0))
        signatures = m.get('record')
        
        with db_session:
            if pe.PersonService.selectByPrimaryKey(enrollId) is None:
                Person(id=enrollId, name=name, rollId=rollId)
            
            if backupnum == 50:
                pass
            
            if en.EnrollInfoService.selectByBackupnum(enrollId, backupnum) is None:
                EnrollInfo(enrollId=enrollId, backupnum=backupnum, signatures=signatures)
        
        x = {
            'ret': 'senduser',
            'result': True,
            'cloudtime': now
        }
        ms = json.dumps(x)
        WebSocketPool.sendMessageToDevice(cli, server, ms)
        deviceStatus.deviceSn = sn
        deviceStatus.status = 1
        deviceStatus.webSocket = server
        deviceStatus.client = cli
        WebSocketPool.addDeviceAndStatus(sn, deviceStatus)
        
def getUserList(cli, server, m):
    userTemps: list[UserTemp] = []
    result = bool(m.get('result', False))
    records = m.get('record', [])
    sn = m.get('sn')
    deviceStatus = DeviceStatus()
    count = 0
    
    if result == True:
        count = int(m.get('count', 0))
        if count > 0:
            for o in records:
                enrollid = int(o.get('enrollid', 0))
                admin = int(o.get('admin', 0))
                backupnum = int(o.get('backupnum', 0))
                userTemp = UserTemp()
                userTemp.enrollId = enrollid
                userTemp.backupnum = backupnum
                userTemp.admin = admin
                userTemps.append(userTemp)
                
            x = {
                'cmd': 'getuserlist',
                'stn': False
            }
            ms = json.dumps(x)
            WebSocketPool.sendMessageToDevice(cli, server, ms)
            deviceStatus.deviceSn = sn
            deviceStatus.status = 1
            deviceStatus.webSocket = server
            deviceStatus.client = cli
            WebSocketPool.addDeviceAndStatus(sn, deviceStatus)
            
    with db_session:
        for uTemp in userTemps:
            if pe.PersonService.selectByPrimaryKey(uTemp.enrollId) is None:
                Person(id=uTemp.enrollId, name='', rollId=uTemp.admin)
                
            if en.EnrollInfoService.selectByBackupnum(uTemp.enrollId, uTemp.backupnum) is None:
                EnrollInfo(enrollId=uTemp.enrollId, backupnum=uTemp.backupnum)
            
def getUserInfo(cli, server, m):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result = bool(m.get('result', False))
    sn = m.get('sn')
    flag = False
    
    if result == True:
        backupnum = int(m.get('backupnum', 0))
        signatures1 = m.get('record')
        enrollid = int(m.get('enrollid', 0))
        name = m.get('name')
        admin = int(m.get('admin', 0))
        signatures = m.get('record')
        
        with db_session:
            person = pe.PersonService.selectByPrimaryKey(enrollid)
            enrollInfo = en.EnrollInfoService.selectByBackupnum(enrollid, backupnum)
            
            if backupnum == 50:
                pass
            
            if person is None:
                Person(id=enrollid, name=name, rollId=admin)
                
            elif person is not None:
                pe.PersonService.updateByPrimaryKey(person)
                
            if enrollInfo is None:
                EnrollInfo(enrollId=enrollInfo.enrollId, backupnum=enrollInfo.backupnum, imagePath=enrollInfo.imagePath, signatures=enrollInfo.signatures)
                
            elif enrollInfo is not None:
                enrollInfo.signatures = signatures
                en.EnrollInfoService.updateByPrimaryKeyWithBLOBs(enrollInfo)
            
def getAllLog(cli, server, m):
    result = bool(m.get('result', False))
    # recordAll: list[Records] = []
    sn = m.get('sn')
    records = m.get('record', [])
    deviceStatus = DeviceStatus()
    count = 0
    flag = False
    
    if result == True:
        count = int(m.get('count', 0))
        if count > 0:
            with db_session:
                for o in records:
                    enrollid = int(o.get('enrollid', 0))
                    time = o.get('time')
                    mode = int(o.get('mode', 0))
                    inout = int(o.get('inout', 0))
                    event = int(o.get('event', 0))
                    temperature = 0
                    
                    if o.get('temp') is not None:
                        temperature = float(o.get('temp', 0))
                        temperature = temperature / 100.0
                        temperature = round(temperature * 10) / 10.0
                        
                    Records(enrollId=enrollid, event=event, intout=inout, mode=mode, recordsTime=time, deviceSerialNum=sn, temperature=temperature)
                    # recordAll.append(record)
                
            x = {
                'cmd': 'getalllog',
                'stn': False
            }
            ms = json.dumps(x)
            WebSocketPool.sendMessageToDevice(cli, server, ms)
            deviceStatus.deviceSn = sn
            deviceStatus.status = 1
            deviceStatus.webSocket = server
            deviceStatus.client = cli
            WebSocketPool.addDeviceAndStatus(sn, deviceStatus)
            
    # for recordsTemp in recordAll:
    #     RecordsService.insert(recordsTemp)
        
def getnewLog(cli, server, m):
    result = bool(m.get('result', False))
    # recordAll: list[Records] = []
    sn = m.get('sn')
    records = m.get('record', [])
    deviceStatus = DeviceStatus()
    count = 0
    flag = False
    
    if result == True:
        count = int(m.get('count', 0))
        if count > 0:
            with db_session:
                for o in records:
                    enrollid = int(o.get('enrollid', 0))
                    time = o.get('time')
                    mode = int(o.get('mode', 0))
                    inout = int(o.get('inout', 0))
                    event = int(o.get('event', 0))
                    temperature = 0
                    
                    if o.get('temp') is not None:
                        temperature = float(o.get('temp', 0))
                        temperature = temperature / 100.0
                        temperature = round(temperature * 10) / 10.0
                        
                    Records(enrollId=enrollid, event=event, intout=inout, mode=mode, recordsTime=time, deviceSerialNum=sn, temperature=temperature)
                    # recordAll.append(record)
                
            x = {
                'cmd': 'getnewlog',
                'stn': False
            }
            ms = json.dumps(x)
            WebSocketPool.sendMessageToDevice(cli, server, ms)
            deviceStatus.deviceSn = sn
            deviceStatus.status = 1
            deviceStatus.webSocket = server
            deviceStatus.client = cli
            WebSocketPool.addDeviceAndStatus(sn, deviceStatus)
            
    # for recordsTemp in recordAll:
    #     RecordsService.insert(recordsTemp)

def onMessageReceived(cli, server, msg):
    print(msg)
    print('=====')
    m = json.loads(msg)
    if m.get('cmd') == 'reg':
        try:
            getDeviceInfo(cli, server, m)
            
        except Exception as e:
            x = {
                'ret': 'reg',
                'result': False,
                'reason': 1
            }
            ms = json.dumps(x)
            WebSocketPool.sendMessageToDevice(cli, server, ms)
            logger.error(traceback.format_exc())
        
    elif m.get('cmd') == 'sendlog':
        try:
            getAttandence(cli, server, m)
        
        except Exception as e:
            x = {
                'ret': 'sendlog',
                'result': False,
                'reason': 1
            }
            ms = json.dumps(x)
            WebSocketPool.sendMessageToDevice(cli, server, ms)
            logger.error(traceback.format_exc())
            
    elif m.get('cmd') == 'senduser':
        try:
            getEnrollInfo(cli, server, m)
        
        except Exception as e:
            x = {
                'ret': 'senduser',
                'result': False,
                'reason': 1
            }
            ms = json.dumps(x)
            WebSocketPool.sendMessageToDevice(cli, server, ms)
            logger.error(traceback.format_exc())
            
    elif m.get('cmd') == 'getalllog':
        sn = m.get('deviceSn')
        del m['deviceSn']
        ms = json.dumps(m)
        WebSocketPool.sendMessageToDeviceStatus(sn, ms)
            
    elif m.get('cmd') == 'getnewlog':
        sn = m.get('deviceSn')
        del m['deviceSn']
        ms = json.dumps(m)
        WebSocketPool.sendMessageToDeviceStatus(sn, ms)
        
    elif m.get('cmd') == 'getuserinfo':
        sn = m.get('deviceSn')
        del m['deviceSn']
        ms = json.dumps(m)
        WebSocketPool.sendMessageToDeviceStatus(sn, ms)
        
    elif m.get('cmd') == 'getuserlist':
        sn = m.get('deviceSn')
        del m['deviceSn']
        ms = json.dumps(m)
        WebSocketPool.sendMessageToDeviceStatus(sn, ms) 
        
    elif m.get('ret') == 'getuserlist':
        getUserList(cli, server, m)
        
    elif m.get('ret') == 'getuserinfo':
        getUserInfo(cli, server, m)
    
    elif m.get('ret') == 'setuserinfo':
        pass
        
    elif m.get('ret') == 'getalllog':
        try:
            getAllLog(cli, server, m)
            
        except Exception as e:
            logger.error(traceback.format_exc())
    
    elif m.get('ret') == 'getnewlog':
        try:
            getnewLog(cli, server, m)
            
        except Exception as e:
            logger.error(traceback.format_exc())
    
def onNewClient(cli, server):
    pass

server = WebsocketServer(host='192.168.5.164', port=7788, loglevel=logging.INFO)
server.set_fn_message_received(onMessageReceived)
server.set_fn_new_client(onNewClient)
server.run_forever()