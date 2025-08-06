# tests/testCli.py
import unittest
from modules.device.network import Network
from modules.cli.cli import CLI
from modules.cli.commands import CommandHandler

class TestCli(unittest.TestCase):
    def setUp(self):
        self.network = Network()
        self.router = self.network.addDevice("router", "Router1")
        self.cli = CLI(self.network)
        self.commandHandler = CommandHandler(self.cli)
    
    def testCommandParsing(self):
        from modules.cli.parser import CommandParser
        parser = CommandParser(self.cli)
        
        command, args = parser.parse("connect g0/0 Switch1 g0/1")
        self.assertEqual(command, "connect")
        self.assertEqual(args, ["g0/0", "Switch1", "g0/1"])
    
    def testPromptGeneration(self):
        from modules.cli.prompts import PromptManager
        promptManager = PromptManager(self.cli)
        
        self.cli.currentDevice = self.router
        self.cli.mode = "user"
        self.assertEqual(promptManager.getPrompt(), "\x1b[32mRouter1>\x1b[0m ")
        
        self.cli.mode = "privileged"
        self.assertEqual(promptManager.getPrompt(), "\x1b[34mRouter1#\x1b[0m ")

if __name__ == '__main__':
    unittest.main()