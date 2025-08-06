# modules/stats/reports.py
from colorama import Fore, Style

class ReportGenerator:
    @staticmethod
    def generateDeviceHistory(device):
        if device.packetHistory.isEmpty():
            return "No hay paquetes recibidos en este dispositivo"
        
        report = []
        tempStack = []
        
        while not device.packetHistory.isEmpty():
            tempStack.append(device.packetHistory.pop())
        
        for i, packet in enumerate(reversed(tempStack), 1):
            report.append(
                f"{i}) From {packet.source} to {packet.destination}: \"{packet.content}\"\n"
                f"   TTL at arrival: {packet.ttl} | Path: {packet.getPathStr()}"
            )
        
        for packet in tempStack:
            device.packetHistory.push(packet)
        
        return "\n".join(report)
    
    @staticmethod
    def generateNetworkStatistics(stats):
        if not stats:
            return "No hay estadísticas disponibles"
        
        report = [
            f"{Fore.CYAN}=== Network Statistics ===",
            f"{Fore.WHITE}Total packets sent: {stats.totalPacketsSent}",
            f"Packets delivered: {stats.packetsDelivered}",
            f"Packets dropped (TTL): {stats.packetsDroppedTtl}",
            f"Packets blocked: {stats.packetsBlocked}"
        ]
        
        if stats.totalPacketsSent > 0:
            avgHops = stats.totalHops / stats.packetsDelivered if stats.packetsDelivered > 0 else 0
            report.append(f"Average hops per packet: {avgHops:.1f}")
        
        if stats.deviceActivity:
            topDevice = max(stats.deviceActivity.items(), key=lambda x: x[1])
            report.append(f"Top talker: {topDevice[0]} ({topDevice[1]} packets processed)")
        
        report.append(Style.RESET_ALL)
        return "\n".join(report)