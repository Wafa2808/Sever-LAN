# tests/testDevices.py
import unittest
from modules.device.network import Network
from modules.device.device import Device

class TestDevices(unittest.TestCase):
    def setUp(self):
        self.network = Network()
        self.router = self.network.addDevice("router", "Router1")
        self.router.addInterface("g0/0")
        self.router.setInterfaceIp("g0/0", "192.168.1.1")
        self.router.setInterfaceStatus("g0/0", "up")
        
        self.switch = self.network.addDevice("switch", "Switch1")
        self.switch.addInterface("g0/1")
        self.switch.setInterfaceStatus("g0/1", "up")
    
    def testDeviceCreation(self):
        self.assertEqual(self.router.name, "Router1")
        self.assertEqual(self.router.type, "router")
        self.assertEqual(self.router.status, "online")
    
    def testInterfaceOperations(self):
        self.assertEqual(self.router.interfaces["g0/0"].ipAddress, "192.168.1.1")
        self.assertEqual(self.router.interfaces["g0/0"].status, "up")
    
    def testNetworkConnections(self):
        self.network.connectDevices("Router1", "g0/0", "Switch1", "g0/1")
        
        routerIface = self.router.interfaces["g0/0"]
        switchIface = self.switch.interfaces["g0/1"]
        
        self.assertEqual(routerIface.connectedTo, ("Switch1", "g0/1"))
        self.assertEqual(switchIface.connectedTo, ("Router1", "g0/0"))

if __name__ == '__main__':
    unittest.main()