# main.py
import json
from modules.device.network import Network
from modules.cli.cli import CLI
from modules.persistence.configLoader import ConfigLoader

def createDefaultConfig():
    defaultConfig = {
        "devices": [
            {
                "name": "Router1",
                "type": "router",
                "status": "online",
                "interfaces": [
                    {"name": "g0/0", "ip": "192.168.1.1", "status": "up"},
                    {"name": "g0/1", "ip": "10.0.0.1", "status": "up"}
                ]
            },
            {
                "name": "Switch1",
                "type": "switch",
                "status": "online",
                "interfaces": [
                    {"name": "g0/1", "ip": "", "status": "up"}
                ]
            },
            {
                "name": "PC1",
                "type": "host",
                "status": "online",
                "interfaces": [
                    {"name": "eth0", "ip": "10.0.0.2", "status": "up"}
                ]
            }
        ],
        "connections": [
            ["Router1", "g0/0", "Switch1", "g0/1"],
            ["Router1", "g0/1", "PC1", "eth0"]
        ]
    }
    
    with open("defaultConfig.json", "w") as f:
        json.dump(defaultConfig, f, indent=2)
    return defaultConfig

def main():
    network = Network()
    
    try:
        ConfigLoader.loadFromFile(network, "defaultConfig.json")
    except FileNotFoundError:
        print("Configuración por defecto no encontrada, creando una nueva...")
        createDefaultConfig()
        ConfigLoader.loadFromFile(network, "defaultConfig.json")
    
    cli = CLI(network)
    cli.start()

if __name__ == "__main__":
    main()