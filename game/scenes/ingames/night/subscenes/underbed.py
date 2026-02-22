from pyglet.window import Window
import engine.scenes.subscene as base_subscene
import game.systems.ingames.night.underbed.init as init_system
import game.systems.ingames.night.underbed.processlogic as process_logic_system
import game.features.ingames.night.sight as sight_feature

class UnderBedSubscene(base_subscene.SubScene):
    def __init__(self, window: Window, save: dict, data: dict) -> None:
        super().__init__(window, save, data)
        self.x: int
        self.y: int

        init_system.init_vars(self)
        init_system.init_entities(self)

    def generate_natural_logic(self) -> None:
        sight_feature.generate_natural_logic(self)
        if self.current_cycle == 0 and self.ticks_in_cycle == 2:
            init_system.post_init(self)
    
    def process_interaction(self, logic_data):
        return process_logic_system.process_interaction(self, logic_data)
    
    def process_release_interaction(self, logic_data):
        return process_logic_system.process_release_interaction(self, logic_data)
    
    def process_natural(self, logic):
        return process_logic_system.process_natural(self, logic)