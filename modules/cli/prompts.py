# modules/cli/prompts.py
from colorama import Fore, Style

class PromptManager:
    def __init__(self, cli):
        self.cli = cli
    
    def getPrompt(self):
        if not self.cli.currentDevice:
            return "> "
        
        deviceName = self.cli.currentDevice.name
        mode = self.cli.mode
        configMode = self.cli.configMode
        interface = self.cli.currentInterface
        
        modeSymbols = {
            'user': ('>', Fore.GREEN),
            'privileged': ('#', Fore.BLUE),
            'config': ('(config)#', Fore.MAGENTA),
        }
        
        symbol, color = modeSymbols.get(mode, ('', Fore.WHITE))
        
        if mode == 'config' and configMode == 'interface':
            symbol = f"(config-if-{interface})#"
        
        prompt = f"{color}{deviceName}{symbol}{Style.RESET_ALL}"
        return prompt