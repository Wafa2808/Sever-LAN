# modules/device/device.py
from modules.dataStructures.queue import Queue
from modules.dataStructures.stack import Stack
from .interface import Interface

class Device:
    def __init__(self, deviceType, name="Unnamed"):
        self.type = deviceType.lower()
        self.name = name
        self.interfaces = {}
        self.status = "online"
        self.packetHistory = Stack()
    
    def addInterface(self, name):
        if name in self.interfaces:
            raise ValueError(f"La interfaz {name} ya existe en {self.name}")
        
        self.interfaces[name] = Interface(name)
        self.interfaces[name].queue = Queue()
        return self.interfaces[name]
    
    def setInterfaceIp(self, interfaceName, ip):
        if interfaceName not in self.interfaces:
            raise ValueError(f"La interfaz {interfaceName} no existe en {self.name}")
        
        if ip and len(ip.split('.')) != 4:
            raise ValueError("Formato de IP inválido. Use formato X.X.X.X")
        
        self.interfaces[interfaceName].ipAddress = ip
    
    def setInterfaceStatus(self, interfaceName, status):
        if interfaceName not in self.interfaces:
            raise ValueError(f"La interfaz {interfaceName} no existe en {self.name}")
        
        status = status.lower()
        if status not in ('up', 'down'):
            raise ValueError("Estado debe ser 'up' o 'down'")
        
        self.interfaces[interfaceName].status = status
    
    def connect(self, interfaceName, neighborDevice, neighborInterface):
        if interfaceName not in self.interfaces:
            raise ValueError(f"La interfaz {interfaceName} no existe en {self.name}")
        
        if self.interfaces[interfaceName].status != 'up':
            raise ValueError(f"La interfaz {interfaceName} no está activa (status: down)")
        
        self.interfaces[interfaceName].connectedTo = (neighborDevice.name, neighborInterface)
        neighborDevice.interfaces[neighborInterface].connectedTo = (self.name, interfaceName)
    
    def disconnect(self, interfaceName):
        if interfaceName not in self.interfaces:
            raise ValueError(f"La interfaz {interfaceName} no existe en {self.name}")
        
        if not self.interfaces[interfaceName].connectedTo:
            return
        
        neighborName, neighborIface = self.interfaces[interfaceName].connectedTo
        self.interfaces[interfaceName].connectedTo = None
    
    def showInterfaces(self):
        result = []
        for ifaceName, interface in self.interfaces.items():
            status = "UP" if interface.status == 'up' else "DOWN"
            ip = interface.ipAddress if interface.ipAddress else "unassigned"
            connected = f"connected to {interface.connectedTo[0]}:{interface.connectedTo[1]}" if interface.connectedTo else "not connected"
            result.append(f"{ifaceName}: IP={ip}, Status={status}, {connected}")
        return "\n".join(result)
    
    def __str__(self):
        return f"{self.name} ({self.type}, {self.status})"