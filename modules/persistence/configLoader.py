# modules/persistence/configLoader.py
import json

class ConfigLoader:
    @staticmethod
    def loadFromFile(network, filename):
        with open(filename) as f:
            config = json.load(f)
        
        for deviceName in list(network.devices.keys()):
            network.removeDevice(deviceName)
        
        for deviceData in config["devices"]:
            device = network.addDevice(deviceData["type"], deviceData["name"])
            device.status = deviceData["status"]
            
            for ifaceData in deviceData["interfaces"]:
                device.addInterface(ifaceData["name"])
                if ifaceData["ip"]:
                    device.setInterfaceIp(ifaceData["name"], ifaceData["ip"])
                device.setInterfaceStatus(ifaceData["name"], ifaceData["status"])
        
        for connection in config.get("connections", []):
            device1, iface1, device2, iface2 = connection
            network.connectDevices(device1, iface1, device2, iface2)
        
        return True