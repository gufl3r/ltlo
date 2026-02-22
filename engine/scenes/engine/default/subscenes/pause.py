import engine.scenes.subscene as base_subscene
import engine.systems.engine.global_.subscenes.pause.init as init_system
import engine.systems.engine.global_.subscenes.pause.processlogic as process_logic_system

class PauseSubScene(base_subscene.SubScene):
    FPS = 30
    def __init__(self, window, save, data: dict) -> None:
        super().__init__(window, save, data)
        
        background_entities = data["background"]

        self._entities = background_entities

        init_system.init_entities(self)

    def process_interaction(self, logic_data):
        return process_logic_system.process_interaction(self, logic_data)
    
    def process_release_interaction(self, logic_data):
        return process_logic_system.process_release_interaction(self, logic_data)
    
    def process_natural(self, logic):
        return process_logic_system.process_natural(self, logic)