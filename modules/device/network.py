# modules/device/network.py
from .device import Device

class Network:
    def __init__(self):
        self.devices = {}
        self.statistics = None
    
    def addDevice(self, deviceType, name):
        if name in self.devices:
            raise ValueError(f"El dispositivo {name} ya existe")
        
        validTypes = ['router', 'switch', 'host', 'firewall']
        if deviceType.lower() not in validTypes:
            raise ValueError(f"Tipo de dispositivo inválido. Use: {', '.join(validTypes)}")
        
        self.devices[name] = Device(deviceType.lower(), name)
        return self.devices[name]
    
    def removeDevice(self, name):
        if name not in self.devices:
            raise ValueError(f"El dispositivo {name} no existe")
        
        device = self.devices[name]
        for ifaceName, interface in device.interfaces.items():
            if interface.connectedTo:
                neighborName, neighborIface = interface.connectedTo
                neighbor = self.devices.get(neighborName)
                if neighbor and neighborIface in neighbor.interfaces:
                    neighbor.interfaces[neighborIface].connectedTo = None
        
        del self.devices[name]
    
    def connectDevices(self, device1Name, iface1Name, device2Name, iface2Name):
        if device1Name not in self.devices:
            raise ValueError(f"Dispositivo {device1Name} no encontrado")
        if device2Name not in self.devices:
            raise ValueError(f"Dispositivo {device2Name} no encontrado")
        
        device1 = self.devices[device1Name]
        device2 = self.devices[device2Name]
        
        if iface1Name not in device1.interfaces:
            raise ValueError(f"Interfaz {iface1Name} no existe en {device1Name}")
        if iface2Name not in device2.interfaces:
            raise ValueError(f"Interfaz {iface2Name} no existe en {device2Name}")
        
        if device1.interfaces[iface1Name].status != 'up':
            raise ValueError(f"La interfaz {iface1Name} en {device1Name} no está activa")
        if device2.interfaces[iface2Name].status != 'up':
            raise ValueError(f"La interfaz {iface2Name} en {device2Name} no está activa")
        
        device1.connect(iface1Name, device2, iface2Name)
        device2.connect(iface2Name, device1, iface1Name)
    
    def disconnectDevices(self, device1Name, iface1Name, device2Name, iface2Name):
        if device1Name not in self.devices:
            raise ValueError(f"Dispositivo {device1Name} no encontrado")
        if device2Name not in self.devices:
            raise ValueError(f"Dispositivo {device2Name} no encontrado")
        
        device1 = self.devices[device1Name]
        device2 = self.devices[device2Name]
        
        if iface1Name not in device1.interfaces:
            raise ValueError(f"Interfaz {iface1Name} no existe en {device1Name}")
        if iface2Name not in device2.interfaces:
            raise ValueError(f"Interfaz {iface2Name} no existe en {device2Name}")
        
        if (device1.interfaces[iface1Name].connectedTo != (device2Name, iface2Name) or 
            device2.interfaces[iface2Name].connectedTo != (device1Name, iface1Name)):
            raise ValueError("Las interfaces no están conectadas entre sí")
        
        device1.interfaces[iface1Name].connectedTo = None
        device2.interfaces[iface2Name].connectedTo = None
    
    def listDevices(self):
        return list(self.devices.values())
    
    def getDevice(self, name):
        return self.devices.get(name)
    
    def setDeviceStatus(self, deviceName, status):
        if deviceName not in self.devices:
            raise ValueError(f"Dispositivo {deviceName} no encontrado")
        
        status = status.lower()
        if status not in ('online', 'offline'):
            raise ValueError("Estado debe ser 'online' u 'offline'")
        
        self.devices[deviceName].status = status
    
    def __str__(self):
        return f"Red con {len(self.devices)} dispositivos"