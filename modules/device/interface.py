# modules/device/interface.py
class Interface:
    def __init__(self, name):
        self.name = name
        self.ipAddress = ""
        self.status = "down"
        self.connectedTo = None
        self.queue = None
    
    def __str__(self):
        return f"{self.name}: IP={self.ipAddress}, Status={self.status}, Connected={self.connectedTo}"