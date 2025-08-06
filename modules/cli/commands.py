from colorama import Fore, Style
from modules.packet.communication import Communication

class CommandHandler:
    def __init__(self, cli):
        self.cli = cli
        self.communication = Communication(cli.network)
        
        from modules.stats.statistics import Statistics
        self.communication.statistics = Statistics()
        self.communication.network.statistics = self.communication.statistics
    
    def execute(self, command, args):
        commandMethods = {
            'help': self.help,
            'exit': self.exit,
            'enable': self.enable,
            'disable': self.disable,
            'configure': self.configureTerminal,
            'hostname': self.hostname,
            'interface': self.interface,
            'ip': self.ipAddress,
            'shutdown': self.shutdown,
            'no': self.noShutdown,
            'exit': self.cmdExit,
            'end': self.end,
            'connect': self.connect,
            'disconnect': self.disconnect,
            'set_device_status': self.setDeviceStatus,
            'list_devices': self.listDevices,
            'send': self.send,
            'tick': self.tick,
            'process': self.tick,
            'show': self.show,
            'ping': self.ping,
            'save': self.saveRunningConfig,
            'load': self.loadConfig,
            'console': self.console
        }
        
        if command not in commandMethods:
            raise ValueError(f"Comando '{command}' no reconocido. Escribe 'help' para ayuda.")
        
        commandMethods[command](*args)
    
    def help(self, *args):
        """Muestra ayuda sobre los comandos disponibles"""
        helpText = """
Comandos disponibles:

Modo Usuario (Router>):
  enable          - Entrar en modo privilegiado
  send            - Enviar un paquete (send <srcIp> <dstIp> <message> [ttl])
  ping            - Enviar un ping (ping <dstIp>)
  console         - Cambiar a otro dispositivo (console <device>)
  exit            - Salir del simulador

Modo Privilegiado (Router#):
  configure       - Entrar en modo configuración
  disable         - Volver a modo usuario
  list_devices    - Listar todos los dispositivos
  connect         - Conectar dispositivos (connect <iface1> <device2> <iface2>)
  disconnect      - Desconectar dispositivos (disconnect <iface1> <device2> <iface2>)
  set_device_status - Cambiar estado de dispositivo (set_device_status <device> <online/offline>)
  tick/process    - Avanzar simulación un paso
  show            - Mostrar información (show interfaces, show history, etc.)
  save            - Guardar configuración (save runningConfig)
  load            - Cargar configuración (load config <filename>)

Modo Configuración (Router(config)#):
  hostname        - Cambiar nombre del dispositivo
  interface       - Entrar en modo configuración de interfaz
  exit            - Salir del modo configuración
  end             - Salir al modo privilegiado

Modo Interfaz (Router(config-if)#):
  ip address      - Configurar IP (ip address <ip>)
  shutdown        - Desactivar interfaz
  no shutdown     - Activar interfaz
  exit            - Salir del modo interfaz
"""
        print(helpText)
    
    def exit(self, *args):
        """Salir del simulador"""
        print("Saliendo del simulador...")
        self.cli.running = False
    
    def enable(self, *args):
        """Entrar en modo privilegiado"""
        if self.cli.mode != 'user':
            raise ValueError("Ya estás en modo privilegiado o de configuración")
        
        if not self.cli.currentDevice:
            raise ValueError("No hay dispositivo seleccionado. Use 'console <device>' primero.")
        
        self.cli.changeMode('privileged')
    
    def disable(self, *args):
        """Volver a modo usuario"""
        if self.cli.mode == 'user':
            raise ValueError("Ya estás en modo usuario")
        
        self.cli.changeMode('user')
    
    def configureTerminal(self, *args):
        """Entrar en modo configuración global"""
        if self.cli.mode != 'privileged':
            raise ValueError("Debes estar en modo privilegiado para configurar")
        
        self.cli.changeMode('config', 'global')
    
    def hostname(self, *args):
        """Cambiar nombre del dispositivo"""
        if self.cli.mode not in ('config', 'privileged'):
            raise ValueError("Debes estar en modo de configuración para cambiar el hostname")
        
        if not args:
            raise ValueError("Se requiere un nombre de dispositivo")
        
        newName = args[0]
        
        if not newName.isalnum():
            raise ValueError("El nombre solo puede contener letras y números")
        
        oldName = self.cli.currentDevice.name
        self.cli.network.devices[newName] = self.cli.network.devices.pop(oldName)
        self.cli.currentDevice.name = newName
        
        if self.cli.currentDevice.name == oldName:
            self.cli.currentDevice = self.cli.network.devices[newName]
        
        print(f"Nombre de dispositivo cambiado de {oldName} a {newName}")
    
    def interface(self, *args):
        """Entrar en modo configuración de interfaz"""
        if self.cli.mode != 'config' or self.cli.configMode != 'global':
            raise ValueError("Debes estar en modo de configuración global para configurar interfaces")
        
        if not args:
            raise ValueError("Se requiere el nombre de una interfaz")
        
        interfaceName = args[0]
        
        if interfaceName not in self.cli.currentDevice.interfaces:
            self.cli.currentDevice.addInterface(interfaceName)
            print(f"Interfaz {interfaceName} creada")
        
        self.cli.changeMode('config', 'interface', interfaceName)
    
    def ipAddress(self, *args):
        """Configurar dirección IP en interfaz"""
        if not (self.cli.mode == 'config' and self.cli.configMode == 'interface'):
            raise ValueError("Debes estar en modo configuración de interfaz para asignar IP")
        
        if len(args) < 1:
            raise ValueError("Se requiere una dirección IP (ip address <ip>)")
        
        ip = args[0]
        self.cli.currentDevice.setInterfaceIp(self.cli.currentInterface, ip)
        print(f"IP {ip} asignada a {self.cli.currentInterface}")
    
    def shutdown(self, *args):
        """Desactivar interfaz"""
        if not (self.cli.mode == 'config' and self.cli.configMode == 'interface'):
            raise ValueError("Debes estar en modo configuración de interfaz para desactivarla")
        
        self.cli.currentDevice.setInterfaceStatus(self.cli.currentInterface, 'down')
        print(f"Interfaz {self.cli.currentInterface} desactivada (shutdown)")
    
    def noShutdown(self, *args):
        """Activar interfaz"""
        if not (self.cli.mode == 'config' and self.cli.configMode == 'interface'):
            raise ValueError("Debes estar en modo configuración de interfaz para activarla")
        
        self.cli.currentDevice.setInterfaceStatus(self.cli.currentInterface, 'up')
        print(f"Interfaz {self.cli.currentInterface} activada (no shutdown)")
    
    def cmdExit(self, *args):
        """Salir del modo actual"""
        if self.cli.mode == 'user':
            self.exit()
        elif self.cli.mode == 'privileged':
            self.disable()
        elif self.cli.mode == 'config':
            self.cli.exitConfigMode()
    
    def end(self, *args):
        """Salir al modo privilegiado desde cualquier modo de configuración"""
        if self.cli.mode == 'config':
            self.cli.endConfigMode()
    
    def connect(self, *args):
        """Conectar dos dispositivos"""
        if self.cli.mode != 'privileged':
            raise ValueError("Debes estar en modo privilegiado para conectar dispositivos")
        
        if len(args) != 3:
            raise ValueError("Uso: connect <iface1> <device2> <iface2>")
        
        iface1, device2, iface2 = args
        device1 = self.cli.currentDevice.name
        
        self.cli.network.connectDevices(device1, iface1, device2, iface2)
        print(f"Conectado {device1}:{iface1} a {device2}:{iface2}")
    
    def disconnect(self, *args):
        """Desconectar dos dispositivos"""
        if self.cli.mode != 'privileged':
            raise ValueError("Debes estar en modo privilegiado para desconectar dispositivos")
        
        if len(args) != 3:
            raise ValueError("Uso: disconnect <iface1> <device2> <iface2>")
        
        iface1, device2, iface2 = args
        device1 = self.cli.currentDevice.name
        
        self.cli.network.disconnectDevices(device1, iface1, device2, iface2)
        print(f"Desconectado {device1}:{iface1} de {device2}:{iface2}")
    
    def setDeviceStatus(self, *args):
        """Cambiar estado de un dispositivo"""
        if self.cli.mode != 'privileged':
            raise ValueError("Debes estar en modo privilegiado para cambiar estado de dispositivos")
        
        if len(args) != 2:
            raise ValueError("Uso: set_device_status <device> <online/offline>")
        
        deviceName, status = args
        self.cli.network.setDeviceStatus(deviceName, status)
        print(f"Estado de {deviceName} cambiado a {status}")
    
    def listDevices(self, *args):
        """Listar todos los dispositivos en la red"""
        if self.cli.mode != 'privileged':
            raise ValueError("Debes estar en modo privilegiado para listar dispositivos")
        
        devices = self.cli.network.listDevices()
        print("\nDispositivos en la red:")
        for device in devices:
            status = Fore.GREEN + "online" + Style.RESET_ALL if device.status == 'online' else Fore.RED + "offline" + Style.RESET_ALL
            print(f" - {device.name} ({device.type}, {status})")
    
    def send(self, *args):
        """Enviar un paquete"""
        if self.cli.mode != 'user':
            raise ValueError("Debes estar en modo usuario para enviar paquetes")
        
        if len(args) < 3:
            raise ValueError("Uso: send <srcIp> <dstIp> <message> [ttl]")
        
        srcIp = args[0]
        dstIp = args[1]
        message = " ".join(args[2:-1]) if len(args) > 3 else args[2]
        ttl = int(args[-1]) if len(args) > 3 and args[-1].isdigit() else 10
        
        try:
            packet = self.communication.sendPacket(srcIp, dstIp, message, ttl)
            print(f"Mensaje encolado para entrega. TTL={ttl}")
        except ValueError as e:
            raise ValueError(f"Error al enviar paquete: {e}")
    
    def tick(self, *args):
        """Procesar un paso de simulación"""
        if self.cli.mode != 'privileged':
            raise ValueError("Debes estar en modo privilegiado para avanzar la simulación")
        
        self.communication.processTick()
        print("[Tick] Procesados todos los paquetes en cola")
    
    def show(self, *args):
        """Mostrar información de red"""
        if not args:
            raise ValueError("Uso: show <interfaces|history|queue|statistics>")
        
        subcommand = args[0].lower()
        
        if subcommand == 'interfaces':
            if not self.cli.currentDevice:
                raise ValueError("No hay dispositivo seleccionado")
            
            print(f"\nInterfaces de {self.cli.currentDevice.name}:")
            print(self.cli.currentDevice.showInterfaces())
        
        elif subcommand == 'history':
            deviceName = args[1] if len(args) > 1 else self.cli.currentDevice.name
            device = self.cli.network.getDevice(deviceName)
            
            if not device:
                raise ValueError(f"Dispositivo {deviceName} no encontrado")
            
            print(f"\nHistorial de paquetes en {deviceName}:")
            if device.packetHistory.isEmpty():
                print("No hay paquetes recibidos")
            else:
                tempStack = []
                while not device.packetHistory.isEmpty():
                    tempStack.append(device.packetHistory.pop())
                
                for i, packet in enumerate(reversed(tempStack), 1):
                    print(f"{i}) De {packet.source} a {packet.destination}: \"{packet.content}\"")
                    print(f"   TTL al llegar: {packet.ttl} | Ruta: {packet.getPathStr()}")
                
                for packet in tempStack:
                    device.packetHistory.push(packet)
        
        elif subcommand == 'queue':
            if not self.cli.currentDevice:
                raise ValueError("No hay dispositivo seleccionado")
            
            interfaceName = args[1] if len(args) > 1 else None
            
            if not interfaceName:
                print(f"\nColas de paquetes en {self.cli.currentDevice.name}:")
                for ifaceName, interface in self.cli.currentDevice.interfaces.items():
                    queueSize = len(interface.queue)
                    print(f" - {ifaceName}: {queueSize} paquetes en cola")
            else:
                if interfaceName not in self.cli.currentDevice.interfaces:
                    raise ValueError(f"Interfaz {interfaceName} no encontrada")
                
                queue = self.communication.showQueue(self.cli.currentDevice.name, interfaceName)
                print(f"\nPaquetes en cola de {self.cli.currentDevice.name}:{interfaceName}:")
                for i, packet in enumerate(queue, 1):
                    print(f"{i}) {packet}")
        
        elif subcommand == 'statistics':
            if not self.communication.statistics:
                print("Estadísticas no disponibles")
                return
            
            stats = self.communication.statistics
            print("\nEstadísticas de red:")
            print(f" - Paquetes enviados: {stats.totalPacketsSent}")
            print(f" - Paquetes entregados: {stats.packetsDelivered}")
            print(f" - Paquetes descartados (TTL): {stats.packetsDroppedTtl}")
            
            if stats.totalPacketsSent > 0:
                avgHops = stats.totalHops / stats.packetsDelivered if stats.packetsDelivered > 0 else 0
                print(f" - Promedio de saltos: {avgHops:.1f}")
            
            if stats.deviceActivity:
                topDevice = max(stats.deviceActivity.items(), key=lambda x: x[1])
                print(f" - Dispositivo más activo: {topDevice[0]} ({topDevice[1]} paquetes procesados)")
        
        else:
            raise ValueError(f"Subcomando '{subcommand}' no reconocido para 'show'")
    
    def ping(self, *args):
        """Enviar un ping"""
        if self.cli.mode != 'user':
            raise ValueError("Debes estar en modo usuario para enviar pings")
        
        if not args:
            raise ValueError("Uso: ping <dstIp>")
        
        dstIp = args[0]
        
        srcIp = None
        for ifaceName, interface in self.cli.currentDevice.interfaces.items():
            if interface.ipAddress:
                srcIp = interface.ipAddress
                break
        
        if not srcIp:
            raise ValueError("El dispositivo actual no tiene IP configurada en ninguna interfaz")
        
        self.send(srcIp, dstIp, "PING", 8)
        print(f"Ping enviado a {dstIp} desde {srcIp}")
    
    def saveRunningConfig(self, *args):
        """Guardar configuración actual"""
        if self.cli.mode != 'privileged':
            raise ValueError("Debes estar en modo privilegiado para guardar configuración")
        
        filename = args[0] if args else "runningConfig.json"
        
        from modules.persistence.configSaver import ConfigSaver
        ConfigSaver.saveToFile(self.cli.network, filename)
        print(f"Configuración guardada en {filename}")
    
    def loadConfig(self, *args):
        """Cargar configuración desde archivo"""
        if self.cli.mode != 'privileged':
            raise ValueError("Debes estar en modo privilegiado para cargar configuración")
        
        if not args:
            raise ValueError("Uso: load config <filename>")
        
        if args[0] != 'config':
            raise ValueError("Uso: load config <filename>")
        
        filename = args[1] if len(args) > 1 else "runningConfig.json"
        
        from modules.persistence.configLoader import ConfigLoader
        ConfigLoader.loadFromFile(self.cli.network, filename)
        print(f"Configuración cargada desde {filename}")
    
    def console(self, *args):
        """Cambiar a otro dispositivo"""
        if self.cli.mode != 'user':
            raise ValueError("Solo puedes cambiar de consola en modo usuario")
        
        if not args:
            raise ValueError("Uso: console <device>")
        
        deviceName = args[0]
        device = self.cli.network.getDevice(deviceName)
        
        if not device:
            raise ValueError(f"Dispositivo {deviceName} no encontrado")
        
        self.cli.currentDevice = device
        print(f"Cambiado a consola de {deviceName}")