# modules/packet/communication.py
from .packet import Packet
from modules.dataStructures.queue import Queue

class Communication:
    def __init__(self, network):
        self.network = network
        self.packetQueues = {}
        self.statistics = None
    
    def sendPacket(self, sourceIp, destinationIp, message, ttl=10):
        sourceDevice = None
        sourceInterface = None
        
        for device in self.network.devices.values():
            if device.status != 'online':
                continue
            
            for ifaceName, interface in device.interfaces.items():
                if interface.ipAddress == sourceIp:
                    sourceDevice = device
                    sourceInterface = ifaceName
                    break
            
            if sourceDevice:
                break
        
        if not sourceDevice:
            raise ValueError(f"No se encontró dispositivo con IP {sourceIp}")
        
        packet = Packet(sourceIp, destinationIp, message, ttl)
        packet.addHop(sourceDevice.name)
        
        sourceDevice.interfaces[sourceInterface].queue.enqueue(packet)
        
        if self.statistics:
            self.statistics.updatePacketSent()
        
        return packet
    
    def processTick(self):
        for deviceName, device in self.network.devices.items():
            if device.status != 'online':
                continue
            
            for ifaceName, interface in device.interfaces.items():
                if interface.status != 'up' or not interface.connectedTo:
                    continue
                
                while not interface.queue.isEmpty():
                    packet = interface.queue.dequeue()
                    
                    if packet.isExpired():
                        if self.statistics:
                            self.statistics.updatePacketDroppedTtl()
                        continue
                    
                    packet.addHop(deviceName)
                    
                    destinationReached = False
                    for _, iface in device.interfaces.items():
                        if iface.ipAddress == packet.destination:
                            device.packetHistory.push(packet)
                            if self.statistics:
                                self.statistics.updatePacketDelivered(len(packet.path) - 1)
                                self.statistics.updateDeviceActivity(deviceName)
                            destinationReached = True
                            break
                    
                    if destinationReached:
                        continue
                    
                    neighborName, neighborIface = interface.connectedTo
                    neighbor = self.network.devices.get(neighborName)
                    
                    if neighbor and neighbor.status == 'online':
                        neighborInterface = neighbor.interfaces.get(neighborIface)
                        if neighborInterface and neighborInterface.status == 'up':
                            neighborInterface.queue.enqueue(packet)
                            if self.statistics:
                                self.statistics.updateDeviceActivity(deviceName)
    
    def showQueue(self, deviceName, interfaceName):
        device = self.network.devices.get(deviceName)
        if not device:
            raise ValueError(f"Dispositivo {deviceName} no encontrado")
        
        if interfaceName not in device.interfaces:
            raise ValueError(f"Interfaz {interfaceName} no encontrada en {deviceName}")
        
        queue = device.interfaces[interfaceName].queue
        return list(queue.items) if not queue.isEmpty() else []