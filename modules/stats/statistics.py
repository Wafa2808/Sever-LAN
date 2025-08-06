# modules/stats/statistics.py
class Statistics:
    def __init__(self):
        self.totalPacketsSent = 0
        self.packetsDelivered = 0
        self.packetsDroppedTtl = 0
        self.packetsBlocked = 0
        self.totalHops = 0
        self.deviceActivity = {}
    
    def updatePacketSent(self):
        self.totalPacketsSent += 1
    
    def updatePacketDelivered(self, hops):
        self.packetsDelivered += 1
        self.totalHops += hops
    
    def updatePacketDroppedTtl(self):
        self.packetsDroppedTtl += 1
    
    def updatePacketBlocked(self):
        self.packetsBlocked += 1
    
    def updateDeviceActivity(self, deviceName):
        if deviceName not in self.deviceActivity:
            self.deviceActivity[deviceName] = 0
        self.deviceActivity[deviceName] += 1
    
    def reset(self):
        self.__init__()