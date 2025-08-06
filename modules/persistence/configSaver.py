# modules/persistence/configSaver.py
import json
from datetime import datetime

class ConfigSaver:
    @staticmethod
    def saveToFile(network, filename="runningConfig.json"):
        config = {
            "metadata": {
                "saveDate": datetime.now().isoformat(),
                "deviceCount": len(network.devices)
            },
            "devices": [],
            "connections": []
        }
        
        for device in network.devices.values():
            deviceData = {
                "name": device.name,
                "type": device.type,
                "status": device.status,
                "interfaces": []
            }
            
            for ifaceName, interface in device.interfaces.items():
                ifaceData = {
                    "name": ifaceName,
                    "ip": interface.ipAddress,
                    "status": interface.status,
                    "queueSize": len(interface.queue) if interface.queue else 0
                }
                deviceData["interfaces"].append(ifaceData)
            
            config["devices"].append(deviceData)
        
        for device in network.devices.values():
            for ifaceName, interface in device.interfaces.items():
                if interface.connectedTo:
                    neighborName, neighborIface = interface.connectedTo
                    connection = sorted([
                        (device.name, ifaceName),
                        (neighborName, neighborIface)
                    ])
                    connectionTuple = (connection[0][0], connection[0][1], connection[1][0], connection[1][1])
                    
                    if connectionTuple not in config["connections"]:
                        config["connections"].append(connectionTuple)
        
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        return True