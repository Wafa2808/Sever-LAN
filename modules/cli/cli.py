# modules/cli/cli.py
from .parser import CommandParser
from .commands import CommandHandler
from .prompts import PromptManager
import colorama
from colorama import Fore, Style

colorama.init()

class CLI:
    def __init__(self, network):
        self.network = network
        self.currentDevice = None
        self.mode = "user"
        self.parser = CommandParser(self)
        self.commandHandler = CommandHandler(self)
        self.promptManager = PromptManager(self)
        self.running = True
        self.configMode = None
        self.currentInterface = None
    
    def start(self):
        print(Fore.GREEN + "\n=== Simulador de Red LAN - CLI Estilo Router ===" + Style.RESET_ALL)
        print("Escribe 'help' para ver los comandos disponibles\n")
        
        if self.network.devices:
            self.currentDevice = next(iter(self.network.devices.values()))
        
        while self.running:
            try:
                self.displayPrompt()
                commandInput = input().strip()
                
                if not commandInput:
                    continue
                
                command, args = self.parser.parse(commandInput)
                self.commandHandler.execute(command, args)
                
            except ValueError as e:
                print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
            except KeyboardInterrupt:
                print("\nUsa el comando 'exit' para salir del simulador")
            except Exception as e:
                print(Fore.RED + f"Error inesperado: {e}" + Style.RESET_ALL)
    
    def displayPrompt(self):
        prompt = self.promptManager.getPrompt()
        print(Fore.YELLOW + prompt + Style.RESET_ALL, end=' ')
    
    def changeMode(self, newMode, configMode=None, interface=None):
        self.mode = newMode
        self.configMode = configMode
        self.currentInterface = interface
    
    def exitConfigMode(self):
        if self.configMode == 'interface':
            self.changeMode('privileged', 'global')
        else:
            self.changeMode('privileged')
    
    def endConfigMode(self):
        self.changeMode('privileged')