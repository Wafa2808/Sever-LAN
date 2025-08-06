# modules/packet/packet.py
import uuid
from datetime import datetime

class Packet:
    def __init__(self, sourceIp, destinationIp, message, ttl=10):
        if not sourceIp or not destinationIp:
            raise ValueError("Se requieren IP de origen y destino")
        
        self.id = str(uuid.uuid4())
        self.source = sourceIp
        self.destination = destinationIp
        self.content = message
        self.ttl = int(ttl)
        if self.ttl <= 0:
            raise ValueError("TTL debe ser mayor que 0")
        
        self.path = []
        self.timestamp = datetime.now()
    
    def addHop(self, deviceName):
        self.path.append(deviceName)
        self.ttl -= 1
    
    def isExpired(self):
        return self.ttl <= 0
    
    def getPathStr(self):
        return " → ".join(self.path) if self.path else "N/A"
    
    def __str__(self):
        return (f"Packet {self.id[:8]}...: {self.source} → {self.destination}, "
                f"TTL={self.ttl}, Path={self.getPathStr()}, "
                f"Content='{self.content[:20]}...'")