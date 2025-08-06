# modules/cli/parser.py
class CommandParser:
    def __init__(self, cli):
        self.cli = cli
    
    def parse(self, commandInput):
        parts = commandInput.split()
        if not parts:
            raise ValueError("Comando vacío")
        
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        return command, args