# tests/testPackets.py
import unittest
from modules.device.network import Network
from modules.packet.packet import Packet
from modules.packet.communication import Communication

class TestPackets(unittest.TestCase):
    def setUp(self):
        self.network = Network()
        self.router = self.network.addDevice("router", "Router1")
        self.router.addInterface("g0/0")
        self.router.setInterfaceIp("g0/0", "192.168.1.1")
        self.router.setInterfaceStatus("g0/0", "up")
        
        self.pc = self.network.addDevice("host", "PC1")
        self.pc.addInterface("eth0")
        self.pc.setInterfaceIp("eth0", "192.168.1.2")
        self.pc.setInterfaceStatus("eth0", "up")
        
        self.network.connectDevices("Router1", "g0/0", "PC1", "eth0")
        
        self.communication = Communication(self.network)
    
    def testPacketCreation(self):
        packet = Packet("192.168.1.1", "192.168.1.2", "Test message", 5)
        self.assertEqual(packet.source, "192.168.1.1")
        self.assertEqual(packet.destination, "192.168.1.2")
        self.assertEqual(packet.ttl, 5)
    
    def testPacketSending(self):
        packet = self.communication.sendPacket("192.168.1.1", "192.168.1.2", "Hello", 5)
        self.assertEqual(packet.source, "192.168.1.1")
        self.assertEqual(packet.destination, "192.168.1.2")
        
        routerIface = self.router.interfaces["g0/0"]
        self.assertFalse(routerIface.queue.isEmpty())
    
    def testPacketProcessing(self):
        self.communication.sendPacket("192.168.1.1", "192.168.1.2", "Hello", 5)
        self.communication.processTick()
        
        self.assertFalse(self.pc.packetHistory.isEmpty())

if __name__ == '__main__':
    unittest.main()