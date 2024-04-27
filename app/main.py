import threading, time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from websocket_server import WebsocketServer
import logging, json

from app.models import DeviceStatus
from app.websocketpool import WebSocketPool
from app import utils

logger = utils.getLogger('main')

app = FastAPI(dependencies=[], title='Wsmypp', description='Wsmyapp API description', version='1.0')
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BackgroundTasks(threading.Thread):
    def run(self,*args,**kwargs):
        while True:
            print('Hello')
            logger.error('kety')
            time.sleep(5)

@app.get('/sendWs/{deviceSn}')
async def sendWs(deviceSn: str):
    message = {
        'cmd': 'getuserlist',
        'stn': True
    }
    WebSocketPool.sendMessageToDeviceStatus(deviceSn, json.dumps(message))
    return {
        'code': 100,
        'msg': 'success'
    }

def onMessageReceived(cli, server, msg):
    print(msg)
    m = json.loads(msg)
    sn = m.get('sn')
    deviceStatus = DeviceStatus('', None, 0)
    deviceStatus.deviceSn = sn
    deviceStatus.status = 1
    deviceStatus.webSocket = cli
    WebSocketPool.addDeviceAndStatus(sn, deviceStatus)
    
def onNewClient(cli, server):
    pass

def main():
    server = WebsocketServer(host='192.168.5.164', port=7788, loglevel=logging.INFO)
    server.set_fn_message_received(onMessageReceived)
    server.set_fn_new_client(onNewClient)
    server.run_forever()

if __name__ == '__main__':
    t = BackgroundTasks()
    t.start()