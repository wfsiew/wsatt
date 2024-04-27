from websocket_server import WebsocketServer
from typing import Dict

from app.models import DeviceStatus

class WebSocketPool:
    
    wsDevice: Dict[str, DeviceStatus] = {}
    
    @classmethod
    def getDeviceSocketBySn(cls, deviceSn: str) -> WebsocketServer:
        deviceStatus: DeviceStatus = cls.wsDevice.get(deviceSn)
        return deviceStatus.webSocket
    
    @classmethod
    def addDeviceAndStatus(cls, deviceSn: str, deviceStatus: DeviceStatus):
        cls.wsDevice[deviceSn] = deviceStatus
        
    @classmethod
    def sendMessageToDeviceStatus(cls, sn: str, message: str):
        deviceStatus: DeviceStatus = cls.wsDevice.get(sn)
        conn: WebsocketServer = deviceStatus.webSocket
        if conn is not None:
            conn.send_message(deviceStatus.client, message)
            
    @classmethod
    def sendMessageToDevice(cls, cli, server: WebsocketServer, message: str):
        server.send_message(cli, message)
            
    @classmethod
    def getDeviceStatus(cls, sn: str) -> DeviceStatus:
        return cls.wsDevice.get(sn)
    
    @classmethod
    def sendMessageToAllDeviceFree(cls, message: str):
        for d in cls.wsDevice.values():
            if d.webSocket is not None:
                d.webSocket.send_message(d.client, message)