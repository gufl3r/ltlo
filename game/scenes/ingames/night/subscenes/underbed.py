from pyglet.window import Window
import engine.scenes.subscene as base_subscene
import game.systems.ingames.night.underbed.init as init_system
import game.systems.ingames.night.underbed.processlogic as process_logic_system

class UnderBedSubscene(base_subscene.SubScene):
    def __init__(self, window: Window, save: dict, data: dict) -> None:
        super().__init__(window, save, data)

    def generate_natural_logic(self) -> None:
        pass
    
    def process_interaction(self, logic_data):
        return process_logic_system.process_interaction(self, logic_data)
    
    def process_release_interaction(self, logic_data):
        return process_logic_system.process_release_interaction(self, logic_data)
    
    def process_natural(self, logic):
        return process_logic_system.process_natural(self, logic)